from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from qb.models import QBDashboardModel
from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer as QBCustomer
import os


class QBDashboard(LoginRequiredMixin, generic.ListView):
    model = QBDashboardModel
    queryset = QBDashboardModel.objects.all()
    template_name = 'qb/index.html'

    # auth_client = AuthClient(
    #     client_id=os.environ.get('QB_CLIENT_ID'),
    #     client_secret=os.environ.get('QB_SECRET'),
    #     environment='sandbox',
    #     redirect_uri='http://localhost:8000/callback',
    # )

    # client = QuickBooks(
    #     auth_client=auth_client,
    #     refresh_token='REFRESH_TOKEN',
    #     company_id=os.environ.get('QB_COMPANY_ID'),
    # )

    # client.sandbox = True

    # qb_customers = QBCustomer.all(qb=client)
