from qb.models import QBSystem


def load_qb_system(request):
    qb_system = QBSystem.objects.last()
    return {'QB_SYSTEM': qb_system}
