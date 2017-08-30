from models import RobotKiller
from django.utils import timezone


max_visits = 100
min_seconds = 600


def anti_bot(request):

    app_ip = request.POST.get('app_id')

    try:
        record = RobotKiller.objects.using('db.sqlite3').get(id=app_ip)
    except RobotKiller.DoesNotExist:
        RobotKiller.objects.using('db.sqlite3').create(id=app_ip, visits=1, time=timezone.now())
        return

    passed_seconds = (timezone.now() - record.time).seconds

    if record.visits > max_visits and passed_seconds < min_seconds:
        raise Exception('user ip banned.')
    else:
        if passed_seconds < min_seconds:
            record.visits = record.visits + 1
            print record.visits, user_ip
            record.save()
        else:
            record.visits = 1
            record.time = timezone.now()
            record.save()