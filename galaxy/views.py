from django.shortcuts import render
from django.shortcuts import HttpResponse, Http404
from models import Galaxy
from django.utils import timezone
import requests
import json
import os

# Create your views here.


def user_galaxy(request, file_name, file_data, ids):
    # get guest ip
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        request_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        request_ip = request.META['REMOTE_ADDR']
    id_string = ','.join(str(i) for i in ids)
    url = 'wb-qb-qiniu.xueba100.com/'+file_name
    star = Galaxy.objects.create(ip=request_ip, post_img=url, question_ids=id_string, upload_time=timezone.now())
    star.save()
    id = star.id
    file_path = 'img_cache/'+str(id)+'_'+file_name
    save(file_data, file_path)

    return


def save(data, file_name):
    if data == None:
        return
    folder = file_name.split('/')[0]
    if not os.path.exists(folder):
        os.mkdir(folder)
    file = open(file_name, "wb")
    file.write(data)
    file.flush()
    file.close()


'''
def img_to_url(file_name, file_data):
    url = 'http://10.10.178.163:8086/upload2qiniu'
    data = {
        'bucket': 'wb-qb',
        'hashname': 'false',
        'sync': 'true',
    }
    files = {'userfile': (file_name, file_data, 'application/octet-stream')}
    try:
        res = requests.post(url=url, files=files, data=data)
    except Exception, e:
        print e
    img_url = json.loads(res.text)['data']['url']
    return img_url
'''

'''
# save to local and then upload to qiniu
def img_to_url(file_name, file_data):
    url = 'http://10.10.178.163:8086/upload2qiniu'
    bucket = 'wb-qb'
    prefix = ''
    filename = 'img_cache/'+str(file_name)
    if filename not in os.listdir('img_cache'):
        save(file_data, filename)
    img_url = post(url, bucket, filename, prefix)
    os.remove(filename)
    return img_url


def post(url, bucket, full_filename, prefix, hash_name='false'):
    pure_file=full_filename.split("/")[-1]
    data = {
        'bucket': bucket,
        'prefix': prefix,
        'suffix': '',
        'hashname': hash_name,
        'sync':'true',
        }
    files={
        'userfile':(pure_file,open(full_filename,'rb'),'application/octet-stream'),
       }
    try:
        res = requests.post(url=url, files=files, data=data)
    except Exception, e:
        print e
    # print res.text
    img_url = json.loads(res.text)['data']['url']
    return img_url
'''
'''
def save(data, file_name):
    if data == None:
        return
    file = open(file_name, "wb")
    file.write(data)
    file.flush()
    file.close()'''