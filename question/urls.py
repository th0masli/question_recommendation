#!python
# log/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.home),
    url(r'BingoYouGotIt', views.home),
    url(r'get_question/(\D+)/(\D+)', views.get_question),
    url(r'rec_html', views.rec_html),
]
