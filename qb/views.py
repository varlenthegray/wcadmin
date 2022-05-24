from __future__ import absolute_import

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError

from quickbooks.objects.customer import Customer as qbCustomer
from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files import File
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from qb.services import qbo_api_call
from dotenv import load_dotenv

from customer.models import Customer

import os

load_dotenv()


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


# Create your views here.
def index(request):
    return render(request, 'qb/index.html')


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
        return HttpResponseBadRequest()
    elif state_tok != auth_client.state_token:
        return HttpResponse('unauthorized', status=401)

    auth_code = request.GET.get('code', None)
    realm_id = request.GET.get('realmId', None)
    request.session['realm_id'] = realm_id

    if auth_code is None:
        return HttpResponseBadRequest()

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


def connected(request):
    auth_client = auth_client_def(request)

    return render(request, 'qb/connected.html', context={'openid': False})


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


def revoke(request):
    auth_client = auth_client_def(request)

    try:
        auth_client.revoke()
    except AuthClientError as e:
        print(e.status_code)
        print(e.intuit_tid)
    return HttpResponse('Revoke successful')


def get_qb_customers(request):
    auth_client = auth_client_def(request)

    client = QuickBooks(
        auth_client=auth_client,
        refresh_token=get_refresh_token(),
        company_id=os.environ.get('QB_COMPANY_ID'),
    )

    try:
        customers = qbCustomer.all(qb=client)
        return HttpResponse(customers)
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)


def insert_qb_customers(request):
    auth_client = auth_client_def(request)

    client = QuickBooks(
        auth_client=auth_client,
        refresh_token=get_refresh_token(),
        company_id=os.environ.get('QB_COMPANY_ID'),
    )

    try:
        customers = qbCustomer.all(qb=client)

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

            try:
                existing_cust = Customer.objects.get(first_name=cust.first_name, last_name=cust.last_name)

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

                existing_cust.save()
            except ObjectDoesNotExist:
                cust.save()

        return HttpResponse(customers)
    except QuickbooksException as e:
        return HttpResponse(str(e.error_code) + ' - ' + e.message)
