#!python
# log/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home),
    url(r'get_question/(\D+)/(\D+)', views.get_question),
    url(r'rec_html', views.rec_html),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
