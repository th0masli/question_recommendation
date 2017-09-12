from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
import os

import json
import intfs
import security
from galaxy import views as gviews

# Create your views here.


# @login_required(login_url='/login')
def get_question(request, interface, key):
    #if not security.ip_bot_filter(request):
        #return HttpResponseForbidden()
    sec_filter(request)
    data = {}
    request.encoding = 'utf-8'
    if request.method == 'POST' and key in request.FILES:
        if login_(request):
            post_data = request.FILES.get(key)
            file_name, file_data = post_data.name, post_data.read()
            info, k, q, ids = intfs.choose_interface(file_data, interface)
            gviews.user_galaxy(request, file_name, file_data, ids)
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
    #if not security.ip_bot_filter(request):
        #return HttpResponseForbidden()
    sec_filter(request)

    request.encoding = 'utf-8'
    if request.method == 'POST':
        post_data = request.FILES.get('file')
        file_name, file_data = post_data.name, post_data.read()
        data, ids = intfs.html(file_data)
        gviews.user_galaxy(request, file_name, file_data, ids)

    return render(request, 'recommend.html', data)


@login_required(login_url="/loginh")
def home(request):
    #if not security.ip_bot_filter(request):
        #return HttpResponseForbidden()
    sec_filter(request)

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


def sec_filter(request):
    try:
        security.ip_bot_filter(request)
    except Exception:
        raise PermissionDenied


def star(request):

    return HttpResponse("Hello, I am Star. Who are you?")


def cube(request):

    return HttpResponse("Hello, I am Cube!")