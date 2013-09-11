from django.conf.urls import patterns, url
from django.views.generic import DetailView

from bitsync import views

urlpatterns = patterns('bitsync.views',
    url(r'^$', views.index, name='index'),
    url(r'^link/(?P<link_id>\d+)/$', views.link, name='link'),
    url(r'^item/(?P<item_id>\d+)/$', views.item, name='item'),
    url(r'^key/(?P<key_id>\d+)/$', views.key, name='key'),
)
