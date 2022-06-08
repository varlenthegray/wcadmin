from __future__ import absolute_import

import math
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from dotenv import load_dotenv

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError
from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects.customer import Customer as qbCustomer
from quickbooks.objects.invoice import Invoice as qbInvoice

from dateutil.relativedelta import relativedelta

from customer.models import Customer
from jobsite.models import JobSite
from qb.services import qbo_api_call
from .models import Invoice, InvoiceLine

load_dotenv()

max_per_run = 500  # The maximum amount of data to pull per run with a hard limit of 1000


# View specific function
def get_refresh_token():
    try:
        with open(os.path.join(settings.BASE_DIR, 'qb_refresh_token.txt')) as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def auth_client_def(request):
    return AuthClient(
        os.environ.get('QB_CLIENT_ID'),
        os.environ.get('QB_SECRET'),
        os.environ.get('QB_REDIRECT_URI'),
        os.environ.get('QB_ENVIRONMENT'),
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


# Create your views here.
@login_required
def index(request):
    return render(request, 'qb/index.html')


@login_required
def oauth(request):
    auth_client = AuthClient(
        os.environ.get('QB_CLIENT_ID'),
        os.environ.get('QB_SECRET'),
        os.environ.get('QB_REDIRECT_URI'),
        os.environ.get('QB_ENVIRONMENT'),
    )

    url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
    request.session['state'] = auth_client.state_token
    return redirect(url)


@login_required
def callback(request):
    auth_client = AuthClient(
        os.environ.get('QB_CLIENT_ID'),
        os.environ.get('QB_SECRET'),
        os.environ.get('QB_REDIRECT_URI'),
        os.environ.get('QB_ENVIRONMENT'),
        state_token=request.session.get('state', None),
    )

    state_tok = request.GET.get('state', None)
    error = request.GET.get('error', None)

    if error == 'access_denied':
        return redirect('index')

    if state_tok is None:
        return HttpResponseBadRequest('400 - State Token (Usually a bad QuickBooks login attempt, please log in again.)')
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
        print(e.status_code)
        print(e.content)
        print(e.intuit_tid)
    except Exception as e:
        print(e)
    return redirect('connected')


@login_required
def connected(request):
    auth_client = auth_client_def(request)

    return render(request, 'qb/connected.html', context={'openid': False})


@login_required
def qbo_request(request):
    auth_client = auth_client_def(request)

    if auth_client.access_token is not None:
        access_token = auth_client.access_token

    if auth_client.realm_id is None:
        raise ValueError('Realm id not specified.')

    response = qbo_api_call(auth_client.access_token, auth_client.realm_id)

    if not response.ok:
        return HttpResponse(' '.join([response.content, str(response.status_code)]))
    else:
        return HttpResponse(response.content)


@login_required
def user_info(request):
    auth_client = auth_client_def(request)

    try:
        response = auth_client.get_user_info()
    except ValueError:
        return HttpResponse('id_token or access_token not found.')
    except AuthClientError as e:
        print(e.status_code)
        print(e.intuit_tid)
    return HttpResponse(response.content)


@login_required
def refresh(request):
    auth_client = auth_client_def(request)

    try:
        auth_client.refresh()

        with open(os.path.join(settings.BASE_DIR, 'qb_refresh_token.txt'), 'w') as f:
            myfile = File(f)
            myfile.write(auth_client.refresh_token)
    except AuthClientError as e:
        print(e.status_code)
        print(e.intuit_tid)

    return HttpResponse('New refresh_token: {0}'.format(auth_client.refresh_token))


@transaction.atomic
@login_required
def insert_qb_customers(request):
    client = qb_client(request)

    try:
        qb_customer_count = qbCustomer.count("Active in (True, False)", qb=client)
        print(f"Customer Count: {qb_customer_count}")
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)
    else:
        runs = math.ceil(qb_customer_count / max_per_run) + 1

        for current_run in range(1, runs):
            print(f"Current Run: {current_run}")
            start_count = (current_run * max_per_run) - max_per_run
            customers = qbCustomer.query(f"SELECT * FROM Customer WHERE Active in (True, False) STARTPOSITION {start_count} MAXRESULTS {max_per_run}",
                                         qb=client)

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
                    is_active=customer.Active
                )

                if customer.PrimaryEmailAddr:
                    cust.email = customer.PrimaryEmailAddr.Address

                if customer.BillAddr:
                    cust.billing_address_1 = customer.BillAddr.Line1
                    cust.billing_address_2 = customer.BillAddr.Line2
                    cust.billing_city = customer.BillAddr.City
                    cust.billing_state = customer.BillAddr.CountrySubDivisionCode
                    cust.billing_zip = customer.BillAddr.PostalCode

                print(f">> Found {cust.first_name} {cust.last_name}")

                try:
                    existing_cust = Customer.objects.get(quickbooks_id=customer.Id)
                except ObjectDoesNotExist:
                    if not customer.ParentRef:
                        cust.save()
                    else:
                        print(f"Not saving {cust.first_name} {cust.last_name} because it has a parent ref of {customer.ParentRef.value}")
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
                            address=cust.billing_address_1,
                            address_2=cust.billing_address_2,
                            city=cust.billing_city,
                            state=cust.billing_state,
                            zip=cust.billing_zip,
                            phone_number=cust.main_phone,
                            email=cust.email,
                            active=cust.is_active,
                            customer=job_customer
                        )

                        new_job_site.save()
                    else:
                        existing_job_site.quickbooks_id = cust.quickbooks_id
                        existing_job_site.address = cust.billing_address_1
                        existing_job_site.address_2 = cust.billing_address_2
                        existing_job_site.city = cust.billing_city
                        existing_job_site.state = cust.billing_state
                        existing_job_site.zip = cust.billing_zip
                        existing_job_site.phone_number = cust.main_phone
                        existing_job_site.email = cust.email
                        existing_job_site.active = cust.is_active

                        existing_job_site.save()

    return HttpResponse('Successfully updated all customers and job sites.')


@login_required
def revoke(request):
    auth_client = auth_client_def(request)

    try:
        auth_client.revoke()
    except AuthClientError as e:
        print(e.status_code)
        print(e.intuit_tid)
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
def get_service_data(request):
    client = qb_client(request)

    try:
        invoice_count = qbInvoice.count(qb=client)
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)
    else:
        runs = math.ceil(invoice_count / max_per_run) + 1

        for current_run in range(1, runs):
            start_count = (current_run * max_per_run) - max_per_run
            invoices = qbInvoice.query(
                f"SELECT * FROM Invoice STARTPOSITION {start_count} MAXRESULTS {max_per_run}",
                qb=client)

            for invoice in invoices:
                try:
                    job_site = JobSite.objects.get(quickbooks_id=invoice.CustomerRef.value)
                except ObjectDoesNotExist:
                    print(f"Unable to locate job site for QB CustomerRef {invoice.CustomerRef.value}")
                else:
                    try:
                        existing_invoice = Invoice.objects.get(invoice_num=invoice.DocNumber)
                    except ValueError:
                        print(f"Error with QB DocNumber {invoice.DocNumber}, ObjectDoesNotExist.")
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
                                    if cf.Name == 'Set Service Int' \
                                            and cf.StringValue != '' and cf.StringValue.isnumeric():
                                        create_invoice.service_interval = cf.StringValue

                            create_invoice.save()

                            if invoice.Line:
                                for invoice_line in invoice.Line:
                                    if invoice_line.DetailType == 'SalesItemLineDetail' \
                                            and invoice_line.Id and invoice_line.Description:
                                        line = InvoiceLine(
                                            line_id=invoice_line.Id,
                                            description=invoice_line.Description,
                                            price=invoice_line.Amount,
                                            invoice=create_invoice
                                        )

                                        line.save()
                    else:
                        # On error of page, for instance not enough records, comment the block out below.
                        # FIXME: Move this to a new view def to "update existing records"
                        existing_invoice.invoice_date = invoice.TxnDate
                        existing_invoice.total = invoice.TotalAmt
                        existing_invoice.job_site = job_site

                        if invoice.CustomerMemo:
                            existing_invoice.memo = invoice.CustomerMemo.value

                        if invoice.CustomField:
                            for cf in invoice.CustomField:
                                if cf.Name == 'Set Service Int' \
                                        and cf.StringValue != '' and cf.StringValue.isnumeric():
                                    existing_invoice.service_interval = cf.StringValue

                        existing_invoice.save()

                        if invoice.Line:
                            for invoice_line in invoice.Line:
                                if invoice_line.DetailType == 'SalesItemLineDetail' \
                                        and invoice_line.Id and invoice_line.Description:
                                    try:
                                        existing_invoice_line = InvoiceLine.objects.get(invoice=existing_invoice,
                                                                                        line_id=invoice_line.Id)
                                    except ObjectDoesNotExist:
                                        line = InvoiceLine(
                                            line_id=invoice_line.Id,
                                            description=invoice_line.Description,
                                            price=invoice_line.Amount,
                                            invoice=existing_invoice
                                        )

                                        line.save()
                                    else:
                                        existing_invoice_line.description = invoice_line.Description
                                        existing_invoice_line.price = invoice_line.Amount

                                        existing_invoice_line.save()

    return HttpResponse('Got data.')


@transaction.atomic
@login_required
def calculate_service_date(request):
    all_jobsites = JobSite.objects.all()

    for jobsite in all_jobsites:
        last_invoice = Invoice.objects.filter(job_site=jobsite).order_by('-invoice_date').first()

        if last_invoice:
            jobsite.next_service_date = last_invoice.invoice_date + relativedelta(months=last_invoice.service_interval)
            jobsite.save()

    return HttpResponse('Success.')
