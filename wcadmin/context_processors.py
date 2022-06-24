import os
from django.conf import settings

from qb.models import QBSystem


def load_qb_system(request):
    qb_system = QBSystem.objects.last()
    return {'QB_SYSTEM': qb_system}


def determine_production_status(request):
    return {'IS_LIVE': os.environ.get('LIVE')}
