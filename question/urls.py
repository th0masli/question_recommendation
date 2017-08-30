#!python
# log/urls.py
from django.conf.urls import url
from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'get_question/(\D+)/(\D+)', views.get_question),
    url(r'rec_html', views.rec_html),
]
