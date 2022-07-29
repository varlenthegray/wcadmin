from __future__ import absolute_import

import math
import os
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone

from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError

from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects.customer import Customer as qbCustomer
from quickbooks.objects.invoice import Invoice as qbInvoice
from quickbooks.objects.item import Item as qbItem
from quickbooks.objects.company_info import CompanyInfo as qbCompanyInfo

from customer.models import Customer, JobSite, JobSiteEquipment
from equipment.models import Equipment

from .models import Invoice, InvoiceLine, QBSystem

load_dotenv()

max_per_run = 500  # The maximum amount of data to pull per run with a hard limit of 1000
logger = logging.getLogger(__name__)


# View specific function
def get_refresh_token():
    try:
        with open(os.path.join(settings.BASE_DIR, 'qb_refresh_token.txt')) as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def auth_client_def(request):
    return AuthClient(
        client_id=os.environ.get('QB_CLIENT_ID'),
        client_secret=os.environ.get('QB_SECRET'),
        redirect_uri=os.environ.get('QB_REDIRECT_URI'),
        environment=os.environ.get('QB_ENVIRONMENT'),
        access_token=request.session.get('access_token', None),
        refresh_token=get_refresh_token(),
        id_token=request.session.get('id_token', None),
        realm_id=request.session.get('realm_id', None),
    )


def qb_client(request):
    return QuickBooks(
        auth_client=auth_client_def(request),
        refresh_token=get_refresh_token(),
        company_id=os.environ.get('QB_COMPANY_ID'),
    )


def save_last_update(request):
    last_update = QBSystem.objects.last()

    if last_update:
        last_update.last_update = timezone.now()

        return last_update.save()
    else:
        current_info = QBSystem(
            last_update=timezone.now(),
            user=request.user,
        )

        return current_info.save()


def create_new_invoice_lines(request, invoice, attach_to_invoice, job_site):
    if invoice.Line:
        for invoice_line in invoice.Line:
            if invoice_line.DetailType == 'SalesItemLineDetail' and invoice_line.Id and invoice_line.Description:
                line = InvoiceLine(
                    line_id=invoice_line.Id,
                    description=invoice_line.Description,
                    price=invoice_line.Amount,
                    invoice=attach_to_invoice,
                )

                try:
                    line.quantity = invoice_line.Qty
                except AttributeError:
                    pass

                line_equipment_id = int(invoice_line.SalesItemLineDetail.ItemRef.value)

                try:
                    line_equipment = Equipment.objects.get(quickbooks_id=line_equipment_id)
                except ObjectDoesNotExist:
                    pass
                else:
                    line.equipment = line_equipment

                    add_equipment_to_job = JobSiteEquipment(
                        installed_on=invoice.TxnDate,
                        added_by=request.user,
                        equipment=line_equipment,
                        job_site=job_site
                    )

                    add_equipment_to_job.save()

                line.save()


def update_create_existing_invoice_lines(request, invoice, attach_to_invoice, job_site):
    if invoice.Line:
        for invoice_line in invoice.Line:
            if invoice_line.DetailType == 'SalesItemLineDetail' and invoice_line.Id and invoice_line.Description:
                try:
                    existing_invoice_line = InvoiceLine.objects.get(invoice=attach_to_invoice, line_id=invoice_line.Id)
                except ObjectDoesNotExist:
                    create_new_invoice_lines(request, invoice, attach_to_invoice, job_site)
                except InvoiceLine.MultipleObjectsReturned:
                    pass
                else:
                    existing_invoice_line.description = invoice_line.Description
                    existing_invoice_line.price = invoice_line.Amount

                    try:
                        existing_invoice_line.quantity = invoice_line.Qty
                    except AttributeError:
                        pass

                    line_equipment_id = int(invoice_line.SalesItemLineDetail.ItemRef.value)

                    try:
                        line_equipment = Equipment.objects.get(quickbooks_id=line_equipment_id)
                    except ObjectDoesNotExist:
                        pass
                    else:
                        existing_invoice_line.equipment = line_equipment

                    existing_invoice_line.save()


def get_last_run():
    system_info = QBSystem.objects.last()

    if system_info:
        return system_info.last_update.isoformat()
    else:
        return timezone.now().isoformat()


# Views
@login_required
def index(request):
    return render(request, 'qb/index.html')


@login_required
def oauth(request):
    auth_client = AuthClient(
        client_id=os.environ.get('QB_CLIENT_ID'),
        client_secret=os.environ.get('QB_SECRET'),
        redirect_uri=os.environ.get('QB_REDIRECT_URI'),
        environment=os.environ.get('QB_ENVIRONMENT'),
    )

    url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
    request.session['state'] = auth_client.state_token
    return redirect(url)


@login_required
def callback(request):
    auth_client = AuthClient(
        client_id=os.environ.get('QB_CLIENT_ID'),
        client_secret=os.environ.get('QB_SECRET'),
        redirect_uri=os.environ.get('QB_REDIRECT_URI'),
        environment=os.environ.get('QB_ENVIRONMENT'),
        state_token=request.session.get('state', None),
    )

    state_tok = request.GET.get('state', None)
    error = request.GET.get('error', None)

    if error == 'access_denied':
        return redirect('index')

    if state_tok is None:
        return HttpResponseBadRequest(
            '400 - State Token (Usually a bad QuickBooks login attempt, please log in again.)')
    elif state_tok != auth_client.state_token:
        return HttpResponse('unauthorized', status=401)

    auth_code = request.GET.get('code', None)
    realm_id = request.GET.get('realmId', None)
    request.session['realm_id'] = realm_id

    if auth_code is None:
        return HttpResponseBadRequest('400 - Auth Code')

    try:
        auth_client.get_bearer_token(auth_code, realm_id=realm_id)
        request.session['access_token'] = auth_client.access_token
        request.session['id_token'] = auth_client.id_token

        with open(os.path.join(settings.BASE_DIR, 'qb_refresh_token.txt'), 'w') as f:
            myfile = File(f)
            myfile.write(auth_client.refresh_token)
    except AuthClientError as e:
        # just printing status_code here but it can be used for retry workflows, etc
        logger.critical(e.status_code)
        logger.critical(e.content)
        logger.critical(e.intuit_tid)
    except Exception as e:
        logger.critical(e)
    return redirect('connected')


@login_required
def connected(request):
    auth_client = auth_client_def(request)

    return render(request, 'qb/connected.html', context={'openid': False})


# @login_required
# def qbo_request(request):
#     auth_client = auth_client_def(request)
#
#     if auth_client.access_token is not None:
#         access_token = auth_client.access_token
#
#     if auth_client.realm_id is None:
#         raise ValueError('Realm id not specified.')
#
#     response = qbo_api_call(auth_client.access_token, auth_client.realm_id)
#
#     if not response.ok:
#         return HttpResponse(str(response.status_code) + ': ' + str(response.content))
#     else:
#         return HttpResponse(response.content)


@login_required
def qbo_request(request):
    client = qb_client(request)

    try:
        company_info = qbCompanyInfo.all(qb=client)
        return HttpResponse(company_info)
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)


@login_required
def user_info(request):
    auth_client = auth_client_def(request)

    try:
        response = auth_client.get_user_info()
    except ValueError:
        return HttpResponse('id_token or access_token not found.')
    except AuthClientError as e:
        logger.critical(e.status_code)
        logger.critical(e.intuit_tid)
    return HttpResponse(response.content)


@login_required
def refresh(request, changes_only=False):
    auth_client = auth_client_def(request)

    try:
        auth_client.refresh()

        with open(os.path.join(settings.BASE_DIR, 'qb_refresh_token.txt'), 'w') as f:
            myfile = File(f)
            myfile.write(auth_client.refresh_token)
    except AuthClientError as e:
        logger.critical(e.status_code)
        logger.critical(e.intuit_tid)

    if changes_only:
        return True
    else:
        return HttpResponse('New refresh_token: {0}'.format(auth_client.refresh_token))


@transaction.atomic
@login_required
def insert_qb_customers(request, changes_only=False):
    client = qb_client(request)
    last_run = get_last_run()

    try:
        if changes_only:
            qb_customer_count = qbCustomer.count(
                f"Active in (True, False) AND Metadata.LastUpdatedTime > '{last_run}'", qb=client
            )
        else:
            qb_customer_count = qbCustomer.count("Active in (True, False)", qb=client)

        # logger.warning(f"{timezone.now()} Customer Update Count: {qb_customer_count}")
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)
    else:
        runs = math.ceil(qb_customer_count / max_per_run) + 1

        for current_run in range(1, runs):
            start_count = (current_run * max_per_run) - max_per_run

            if changes_only:
                # logger.warning("Checking for changes to customers.")
                customers = qbCustomer.query(
                    f"SELECT * FROM Customer WHERE Active in (True, False) AND Metadata.LastUpdatedTime > '{last_run}' STARTPOSITION {start_count} MAXRESULTS {max_per_run}",
                    qb=client
                )
            else:
                # logger.warning("Getting all customer data from Quickbooks.")
                customers = qbCustomer.query(
                    f"SELECT * FROM Customer WHERE Active in (True, False) STARTPOSITION {start_count} MAXRESULTS {max_per_run}",
                    qb=client
                )

            for customer in customers:
                cust = Customer(
                    quickbooks_id=customer.Id,
                    company=customer.CompanyName,
                    title=customer.Title,
                    first_name=customer.GivenName,
                    middle_name=customer.MiddleName,
                    last_name=customer.FamilyName,
                    website=customer.WebAddr,
                    main_phone=customer.PrimaryPhone,
                    alternate_phone=customer.Mobile,
                    fax_number=customer.Fax,
                    is_active=customer.Active,
                    notes=customer.Notes,
                )

                if customer.PrimaryEmailAddr:
                    cust.email = customer.PrimaryEmailAddr.Address

                if customer.BillAddr:
                    cust.billing_address_1 = customer.BillAddr.Line1
                    cust.billing_address_2 = customer.BillAddr.Line2
                    cust.billing_city = customer.BillAddr.City
                    cust.billing_state = customer.BillAddr.CountrySubDivisionCode
                    cust.billing_zip = customer.BillAddr.PostalCode

                if customer.ShipAddr:
                    cust.ship_addr_1 = customer.ShipAddr.Line1
                    cust.ship_addr_2 = customer.ShipAddr.Line2
                    cust.ship_city = customer.ShipAddr.City
                    cust.ship_state = customer.ShipAddr.CountrySubDivisionCode
                    cust.ship_zip = customer.ShipAddr.PostalCode

                try:
                    existing_cust = Customer.objects.get(quickbooks_id=customer.Id)
                except ObjectDoesNotExist:
                    if not customer.ParentRef:
                        cust.save()
                else:
                    existing_cust.quickbooks_id = cust.quickbooks_id
                    existing_cust.company = cust.company
                    existing_cust.title = cust.title
                    existing_cust.website = cust.website
                    existing_cust.email = cust.email
                    existing_cust.main_phone = cust.main_phone
                    existing_cust.alternate_phone = cust.alternate_phone
                    existing_cust.fax_number = cust.fax_number
                    existing_cust.is_active = cust.is_active
                    existing_cust.notes = cust.notes

                    if customer.BillAddr:
                        existing_cust.billing_address_1 = cust.billing_address_1
                        existing_cust.billing_address_2 = cust.billing_address_2
                        existing_cust.billing_city = cust.billing_city
                        existing_cust.billing_state = cust.billing_state
                        existing_cust.billing_zip = cust.billing_zip

                    if not customer.ParentRef:
                        existing_cust.save()
                finally:
                    try:
                        existing_job_site = JobSite.objects.get(quickbooks_id=customer.Id)
                    except ObjectDoesNotExist:
                        if not customer.ParentRef:
                            job_customer = Customer.objects.get(quickbooks_id=customer.Id)
                        else:
                            job_customer = Customer.objects.get(quickbooks_id=customer.ParentRef.value)

                        new_job_site = JobSite(
                            quickbooks_id=cust.quickbooks_id,
                            name=customer.DisplayName,
                            phone_number=cust.main_phone,
                            email=cust.email,
                            active=cust.is_active,
                            customer=job_customer,
                        )

                        if customer.ShipAddr:
                            new_job_site.address = cust.ship_addr_1
                            new_job_site.address_2 = cust.ship_addr_2
                            new_job_site.city = cust.ship_city
                            new_job_site.state = cust.ship_state
                            new_job_site.zip = cust.ship_zip
                        else:
                            new_job_site.address = cust.billing_address_1
                            new_job_site.address_2 = cust.billing_address_2
                            new_job_site.city = cust.billing_city
                            new_job_site.state = cust.billing_state
                            new_job_site.zip = cust.billing_zip

                        new_job_site.save()
                    else:
                        existing_job_site.quickbooks_id = cust.quickbooks_id
                        existing_job_site.phone_number = cust.main_phone
                        existing_job_site.email = cust.email
                        existing_job_site.active = cust.is_active

                        if customer.ShipAddr:
                            existing_job_site.address = cust.ship_addr_1
                            existing_job_site.address_2 = cust.ship_addr_2
                            existing_job_site.city = cust.ship_city
                            existing_job_site.state = cust.ship_state
                            existing_job_site.zip = cust.ship_zip
                        else:
                            existing_job_site.address = cust.billing_address_1
                            existing_job_site.address_2 = cust.billing_address_2
                            existing_job_site.city = cust.billing_city
                            existing_job_site.state = cust.billing_state
                            existing_job_site.zip = cust.billing_zip

                        existing_job_site.save()

    get_equipment_qb(request, changes_only)

    if not changes_only:
        return HttpResponse('Successfully fetched all customers, job sites, and equipment.')
    else:
        pass


@login_required
def revoke(request):
    auth_client = auth_client_def(request)

    try:
        auth_client.revoke()
    except AuthClientError as e:
        logger.critical(e.status_code)
        logger.critical(e.intuit_tid)
    return HttpResponse('Revoke successful')


@login_required
def get_qb_customers(request):
    client = qb_client(request)

    try:
        customers = qbCustomer.all(qb=client)
        return HttpResponse(customers)
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)


@transaction.atomic
@login_required
def get_service_data(request, changes_only=False):
    client = qb_client(request)
    last_run = get_last_run()

    try:
        if changes_only:
            invoice_count = qbInvoice.count(f"Metadata.LastUpdatedTime > '{last_run}'", qb=client)
        else:
            invoice_count = qbInvoice.count(qb=client)

        # logger.warning(f"{timezone.now()} Invoices to Update: {invoice_count}")
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)
    else:
        runs = math.ceil(invoice_count / max_per_run) + 1

        for current_run in range(1, runs):
            start_count = (current_run * max_per_run) - max_per_run

            if changes_only:
                # logger.warning("Checking for service changes.")
                invoices = qbInvoice.query(
                    f"SELECT * FROM Invoice WHERE Metadata.LastUpdatedTime > '{last_run}' STARTPOSITION {start_count} MAXRESULTS {max_per_run}",
                    qb=client)
            else:
                # logger.warning("Updating all service records.")
                invoices = qbInvoice.query(
                    f"SELECT * FROM Invoice STARTPOSITION {start_count} MAXRESULTS {max_per_run}",
                    qb=client)

            for invoice in invoices:
                try:
                    job_site = JobSite.objects.get(quickbooks_id=invoice.CustomerRef.value)
                except ObjectDoesNotExist:
                    logger.warning(f"Unable to locate job site for QB CustomerRef {invoice.CustomerRef.value}")
                else:
                    try:
                        existing_invoice = Invoice.objects.get(invoice_num=invoice.DocNumber)
                    except ValueError:
                        logger.warning(f"Error with QB DocNumber {invoice.DocNumber}, ValueError.")
                    except ObjectDoesNotExist:
                        if invoice.DocNumber:
                            create_invoice = Invoice(
                                invoice_num=invoice.DocNumber,
                                invoice_date=invoice.TxnDate,
                                total=invoice.TotalAmt,
                                job_site=job_site
                            )

                            if invoice.CustomerMemo:
                                create_invoice.memo = invoice.CustomerMemo.value

                            if invoice.CustomField:
                                for cf in invoice.CustomField:
                                    if cf.Name == 'Set Service Int' and cf.StringValue != '' \
                                            and cf.StringValue.isnumeric():
                                        create_invoice.service_interval = int(cf.StringValue)

                                        job_site.service_interval = create_invoice.service_interval

                            next_service = parse(create_invoice.invoice_date).date() + \
                                           relativedelta(months=job_site.service_interval)

                            if job_site.next_service_date:
                                if next_service > job_site.next_service_date:
                                    job_site.next_service_date = next_service
                                    job_site.service_scheduled = False
                            else:
                                job_site.next_service_date = next_service

                            job_site.save()

                            create_invoice.save()

                            create_new_invoice_lines(request, invoice, create_invoice, job_site)
                    else:
                        existing_invoice.invoice_date = invoice.TxnDate
                        existing_invoice.total = invoice.TotalAmt
                        existing_invoice.job_site = job_site

                        if invoice.CustomerMemo:
                            existing_invoice.memo = invoice.CustomerMemo.value

                        if invoice.CustomField:
                            for cf in invoice.CustomField:
                                if cf.Name == 'Set Service Int' and cf.StringValue != '' and cf.StringValue.isnumeric():
                                    existing_invoice.service_interval = int(cf.StringValue)

                                    job_site.service_interval = existing_invoice.service_interval

                        next_service = parse(existing_invoice.invoice_date).date() + \
                                       relativedelta(months=job_site.service_interval)

                        if job_site.next_service_date:
                            if next_service > job_site.next_service_date:
                                job_site.next_service_date = next_service
                                job_site.service_scheduled = False
                        else:
                            job_site.next_service_date = next_service

                        job_site.save()
                        existing_invoice.save()

                        update_create_existing_invoice_lines(request, invoice, existing_invoice, job_site)
    finally:
        save_last_update(request)

    if not changes_only:
        return HttpResponse('Successfully updated all service records, invoices, and associated information.')


@transaction.atomic
@login_required
# ##### DEPRECATED ######
def calculate_service_date(request):
    update_service_interval(request)

    all_jobsites = JobSite.objects.all()

    for jobsite in all_jobsites:
        last_invoice = Invoice.objects.filter(job_site=jobsite).order_by('-invoice_date').first()

        if last_invoice:
            jobsite.next_service_date = last_invoice.invoice_date + relativedelta(months=jobsite.service_interval)
            jobsite.save()

    save_last_update(request)

    return HttpResponse('Successfully calculated service dates.')


@login_required
def get_equipment_qb(request, changes_only=False):
    client = qb_client(request)
    last_run = get_last_run()

    try:
        if changes_only:
            item_count = qbItem.count(
                f"ParentRef in ('316', '318') AND Metadata.LastUpdatedTime > '{last_run}'", qb=client
            )
        else:
            item_count = qbItem.count("ParentRef in ('316', '318')", qb=client)

        # logger.warning(f"{timezone.now()} Equipment to update: {item_count}")
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)
    else:
        runs = math.ceil(item_count / max_per_run) + 1

        for current_run in range(1, runs):
            start_count = (current_run * max_per_run) - max_per_run

            if changes_only:
                # logger.warning("Checking equipment for latest changes.")
                items = qbItem.query(
                    f"SELECT * FROM Item WHERE ParentRef IN ('316', '318') AND Metadata.LastUpdatedTime > '{last_run}' STARTPOSITION {start_count} MAXRESULTS {max_per_run}",
                    qb=client)
            else:
                # logger.warning("Updating all equipment.")
                items = qbItem.query(
                    f"SELECT * FROM Item WHERE ParentRef IN ('316', '318') STARTPOSITION {start_count} MAXRESULTS {max_per_run}",
                    qb=client)

            for item in items:
                add_item = Equipment(
                    sales_price=item.UnitPrice,
                    cost=item.PurchaseCost,
                    is_active=item.Active,
                    quickbooks_id=item.Id,
                    last_updated_by=request.user,
                )

                if item.Sku:
                    add_item.sku = item.Sku

                if item.Description:
                    add_item.description = item.Description

                if item.PurchaseDesc:
                    add_item.name = item.PurchaseDesc
                else:
                    add_item.name = item.Name

                try:
                    existing_item = Equipment.objects.get(quickbooks_id=item.Id)
                except ObjectDoesNotExist:
                    add_item.save()
                else:
                    existing_item.name = add_item.name
                    existing_item.cost = add_item.cost
                    existing_item.sales_price = add_item.sales_price
                    existing_item.is_active = add_item.is_active
                    existing_item.sku = add_item.sku
                    existing_item.description = add_item.description
                    existing_item.last_updated_by = add_item.last_updated_by

                    existing_item.save()

        if not changes_only:
            return HttpResponse(f"Total Item Count: {item_count}.<br>>>> Updated successfully.")
    finally:
        save_last_update(request)


@transaction.atomic
@login_required
def attach_equipment_to_job_site(request):
    equipment_line_items = InvoiceLine.objects.filter(equipment__isnull=False).select_related()

    for line_equipment in equipment_line_items:
        add_equipment = JobSiteEquipment(
            installed_on=line_equipment.invoice.invoice_date,
            added_by=request.user,
            equipment=line_equipment.equipment,
            job_site=line_equipment.invoice.job_site,
        )

        add_equipment.save()

    return HttpResponse("Successfully tied all equipment to job sites.")


@transaction.atomic
@login_required
def update_service_interval(request):
    # Get all records that do not equal 12 for service interval
    all_non_standard_invoices = Invoice.objects.filter(~Q(service_interval=12)).select_related('job_site')

    for invoice in all_non_standard_invoices:
        invoice.job_site.service_interval = invoice.service_interval
        invoice.job_site.save()

    return HttpResponse("Successfully updated service interval.")


@login_required
def update_db_from_changes(request):
    if refresh(request):
        insert_qb_customers(request, True)
        get_service_data(request, True)

        return HttpResponse(status=200, content='Successfully received changes from QuickBooks.')
    else:
        return HttpResponse(status=400, content='Unable to get changes.')


@login_required
def get_print_on_check_name_from_qb(request):
    client = qb_client(request)
    all_job_sites = JobSite.objects.all()

    try:
        customer_count = qbCustomer.count("Active in (True, False)", qb=client)
        # logger.warning(f"{timezone.now()} Customers getting Print on Check name for: {customer_count}")
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)
    else:
        runs = math.ceil(customer_count / max_per_run) + 1

        for current_run in range(1, runs):
            start_count = (current_run * max_per_run) - max_per_run

            customers = qbCustomer.query(
                f"SELECT * FROM Customer WHERE Active in (True, False) STARTPOSITION {start_count} MAXRESULTS {max_per_run}",
                qb=client
            )

            for customer in customers:
                try:
                    job_site = all_job_sites.get(quickbooks_id=customer.Id)

                    job_site.print_on_check_name = customer.PrintOnCheckName
                    job_site.first_name = customer.GivenName
                    job_site.last_name = customer.FamilyName

                    job_site.save()
                except ObjectDoesNotExist:
                    pass

    return HttpResponse('Successfully updated Job Site Print on Checks name, First Name and Last Name.')


@login_required
def get_qb_created_on(request):
    client = qb_client(request)
    all_job_sites = JobSite.objects.all()
    all_customers = Customer.objects.all()

    try:
        customer_count = qbCustomer.count("Active in (True, False)", qb=client)
        # logger.warning(f"{timezone.now()} Customers getting created date for: {customer_count}")
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)
    else:
        runs = math.ceil(customer_count / max_per_run) + 1

        for current_run in range(1, runs):
            start_count = (current_run * max_per_run) - max_per_run

            customers = qbCustomer.query(
                f"SELECT * FROM Customer WHERE Active in (True, False) STARTPOSITION {start_count} MAXRESULTS {max_per_run}",
                qb=client
            )

            for customer in customers:
                create_time = customer.MetaData['CreateTime']

                try:
                    job_site = all_job_sites.get(quickbooks_id=customer.Id)

                    job_site.qb_created_on = create_time

                    job_site.save()
                except ObjectDoesNotExist:
                    pass
                finally:
                    try:
                        customer = all_customers.get(quickbooks_id=customer.Id)

                        customer.qb_created_on = create_time

                        customer.save()
                    except ObjectDoesNotExist:
                        pass

    return HttpResponse('Successfully updated Job Site and Customers with QB Created Time.')
