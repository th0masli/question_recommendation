"""starcube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from question import views
from django.contrib.auth import views as auth_views
from question.forms import LoginForm

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', views.home),
    url(r'get_question/(\D+)/(\D+)', views.get_question),
    url(r'Easter_Egg0', views.star),
    url(r'Easter_Egg', views.cube),
    url(r'rec_html', views.rec_html),
    url(r'', include('question.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}),
]
