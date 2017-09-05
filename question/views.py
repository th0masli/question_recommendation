from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

import json
import intfs

# Create your views here.


# @login_required(login_url='/login')
def get_question(request, interface, key):
    bot(request)
    data = {}
    request.encoding = 'utf-8'
    if request.method == 'POST' and key in request.FILES and ip_check(request):
        if login_(request):
            post_data = request.FILES.get(key)
            '''
            #call ocr api return ocr result
            #call question description api according to ocr result
            #call matrix condition return questions according to question description
            #calculate similarity. Retrieving questions between thresholds
            '''
            info, k, q = intfs.choose_interface(post_data, interface)
            if info:
                data['msg'] = 'success'
                data['status'] = 0
                data[k] = info
            else:
                data['msg'] = 'nothing to recommend'
                data['status'] = 1
        else:
            data['msg'] = 'incorrect username or password'
            data['status'] = 1

    elif request.method != 'POST':
        data['msg'] = 'method not allowed'
        data['status'] = 1

    elif key not in request.FILES:
        data['msg'] = 'invalid key'
        data['status'] = 1

    elif not ip_check(request):
        data['msg'] = 'ip not allowed'
        data['status'] = 1

    result = json.dumps(data)

    return HttpResponse(result)


@login_required(login_url="/loginh")
def rec_html(request):
    bot(request)
    request.encoding = 'utf-8'
    if request.method == 'POST' and ip_check(request):
        post_data = request.FILES.get('file')
        data = intfs.html(post_data)

    return render(request, 'recommend.html', data)


@login_required(login_url="/loginh")
def home(request):
    bot(request)

    if ip_check(request):

        return render(request, 'home.html')


def star(request):

    return HttpResponse("Hello, I am Star. Who are you?")


def cube(request):

    return HttpResponse("Hello, I am Cube!")


def login_(request):
    app_id = request.POST.get('app_id')
    app_key = request.POST.get('app_key')
    user = authenticate(username=app_id, password=app_key)
    if user and user.is_active:
        login(request, user)
        return True
    else:
        return False


def ip_check(request):
    allow_ips = ['10', '127.0.0.1'] # localhost
    # allow_ips = ['10', '60.205.107.184']
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    # print ip
    if ip[:2] in allow_ips or ip in allow_ips:
        return True
    return False


def bot(request):
    try:
        anti_bot(request)
    except Exception, e:
        if unicode(e) == 'user ip banned.':
            raise PermissionDenied()