import os

from django.core.exceptions import ObjectDoesNotExist

from qb.models import QBSystem
from main.models import VersionLog
from users.models import Preferences


def load_qb_system(request):
    qb_system = QBSystem.objects.last()
    return {'QB_SYSTEM': qb_system}


def determine_production_status(request):
    return {'IS_LIVE': os.environ.get('LIVE')}


def get_version_info(request):
    full_version_log = VersionLog.objects.all().order_by('-pk')
    latest_version = VersionLog.objects.last()
    return {'VERSION_LOG': full_version_log, 'LATEST_VERSION': latest_version}


def get_theme(request):
    if request.user.is_authenticated:
        try:
            preferences = Preferences.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return {'THEME': 'demo2'}
        else:
            return {'THEME': preferences.theme}
    else:
        return {'THEME': 'demo2'}
