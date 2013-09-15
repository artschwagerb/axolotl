from django.conf.urls import patterns, url
from django.views.generic import DetailView

from tv import views

urlpatterns = patterns('tv.views',
    url(r'^$', views.index, name='tv-index'),
    url(r'^show/(?P<pk>\d+)/$', views.show, name='tv-show'),
    url(r'^season/(?P<pk>\d+)/$', views.season, name='tv-season'),
    url(r'^episode/(?P<pk>\d+)/$', views.episode, name='tv-episode'),
    url(r'^episode/(?P<pk>\d+)/update/$', views.episode_update, name='tv-episode-update'),
    url(r'^search', views.search, name='tv-search'),
)
