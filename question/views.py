from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

import json
import intfs
import security

# Create your views here.


# @login_required(login_url='/login')
def get_question(request, interface, key):
    if not security.ip_bot_filter(request):
        return HttpResponseForbidden()
    data = {}
    request.encoding = 'utf-8'
    if request.method == 'POST' and key in request.FILES:
        if login_(request):
            post_data = request.FILES.get(key)
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

    result = json.dumps(data)

    return HttpResponse(result)


@login_required(login_url="/loginh")
def rec_html(request):
    if not security.ip_bot_filter(request):
        return HttpResponseForbidden()

    request.encoding = 'utf-8'
    if request.method == 'POST':
        post_data = request.FILES.get('file')
        data = intfs.html(post_data)

    return render(request, 'recommend.html', data)


@login_required(login_url="/loginh")
def home(request):
    if not security.ip_bot_filter(request):
        return HttpResponseForbidden()

    return render(request, 'home.html')


def login_(request):
    app_id = request.POST.get('app_id')
    app_key = request.POST.get('app_key')
    user = authenticate(username=app_id, password=app_key)
    if user and user.is_active:
        login(request, user)
        return True
    else:
        return False


def star(request):

    return HttpResponse("Hello, I am Star. Who are you?")


def cube(request):

    return HttpResponse("Hello, I am Cube!")