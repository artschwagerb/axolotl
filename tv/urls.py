from django.conf.urls import patterns, url
from django.views.generic import DetailView

from tv import views

urlpatterns = patterns('tv.views',
    url(r'^$', views.index, name='index'),
    url(r'^show/(?P<show_id>\d+)/$', views.show, name='show'),
    url(r'^season/(?P<season_id>\d+)/$', views.season, name='season'),
    url(r'^episode/(?P<episode_id>\d+)/$', views.episode, name='episode'),
)
