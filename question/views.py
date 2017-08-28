from django.shortcuts import render
from django.shortcuts import HttpResponse

import json
import intfs

# Create your views here.


def get_question(request, interface, key):
    data = {}
    request.encoding = 'utf-8'
    if request.method == 'POST' and key in request.FILES:
        post_data = request.FILES.get(key)
        '''
        call ocr api return ocr result
        call question description api according to ocr result
        call matrix condition return questions according to question description
        calculate similarity. Retrieving questions between thresholds
        '''
        info, k = intfs.choose_interface(post_data, interface)
        if info:
            data['msg'] = 'success'
            data['status'] = 0
            data[k] = info
        else:
            data['msg'] = 'nothing to recommend'
            data['status'] = 1

    elif request.method != 'POST':
        data['msg'] = 'method not allowed'
        data['status'] = 1

    elif key not in request.FILES:
        data['msg'] = 'invalid key'
        data['status'] = 1

    result = json.dumps(data)

    return HttpResponse(result)


def rec_html(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        post_data = request.FILES.get('file')
        data = intfs.html(post_data)

    return render(request, 'recommend.html', data)


def home(request):

    return render(request, 'home.html')


def star(request):

    return HttpResponse("Hello, I am Star. Who are you?")


def cube(request):

    return HttpResponse("Hello, I am Cube!")