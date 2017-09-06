from models import RobotKiller
from django.utils import timezone


max_visits = 100
min_seconds = 300


def ip_bot_filter(request):
    allowed_ips = ['10', '127.0.0.1']  # localhost
    # allowed_ips = ['10', '60.205.107.184']
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        request_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        request_ip = request.META['REMOTE_ADDR']
    # print request_ip
    if request_ip[:2] in allowed_ips or request_ip in allowed_ips:
        try:
            record = RobotKiller.objects.get(ip=request_ip)
        except RobotKiller.DoesNotExist:
            RobotKiller.objects.create(ip=request_ip, visits=1, time=timezone.now(), status='allowed')
            return

        passed_seconds = (timezone.now() - record.time).seconds

        if record.visits > max_visits and passed_seconds < min_seconds and record.status == 'banned':
            record.status = 'banned'
            return False
        else:
            if passed_seconds < min_seconds:
                record.visits = record.visits + 1
                record.save()
            else:
                record.visits = 1
                record.time = timezone.now()
                record.save()
            return True
    else:
        return False


