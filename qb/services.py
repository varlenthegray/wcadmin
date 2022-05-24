import requests
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv()


def qbo_api_call(access_token, realm_id):
    """[summary]

    """

    if os.environ.get('QB_ENVIRONMENT') == 'production':
        base_url = settings.QBO_BASE_PROD
    else:
        base_url = settings.QBO_BASE_SANDBOX

    route = '/v3/company/{0}/companyinfo/{0}'.format(realm_id)
    auth_header = 'Bearer {0}'.format(access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json'
    }
    return requests.get('{0}{1}'.format(base_url, route), headers=headers)
