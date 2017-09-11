from django.shortcuts import render
from django.shortcuts import HttpResponse, Http404
from models import Galaxy
from django.utils import timezone
from question import intfs
import requests
import json

# Create your views here.


def user_galaxy(request, ids):
    img_file = request.FILES.get('file')
    # get guest ip
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        request_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        request_ip = request.META['REMOTE_ADDR']
    id_string = ','.join(str(i) for i in ids)
    url = img_to_url(img_file)
    star = Galaxy.objects.create(ip=request_ip, post_img=url, question_ids=id_string, upload_time=timezone.now())
    star.save()

    return


def img_to_url(value):
    url = 'http://10.10.178.163:8086/upload2qiniu'
    data = {
        'bucket': 'wb-qb',
        'suffix': '',
        'prefix': '/galaxy',
        'hashname': 'false',
        'sync': 'true',
    }
    files = {'userfile': (str(value), value, 'application/octet-stream')}
    try:
        res = requests.post(url=url, files=files, data=data)
    except Exception, e:
        print e
    res = json.loads(res.text)
    return res['data']['url']

