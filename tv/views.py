# Create your views here.
import urllib2
import json
import hashlib
import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import timezone

from datetime import datetime, timedelta

from django.conf import settings

from tv.models import *

from django.db.models import Q

@login_required
def index(request):
	show_list = Show.objects.order_by('name')
	template = loader.get_template('tv_index.html')
	context = RequestContext(request, {
		'show_list': show_list,
	})
	return HttpResponse(template.render(context))

@login_required
def show_favorites(request):
	fav_list = Show_Favorite.objects.filter(user=request.user,active=True).order_by('show__name')
	template = loader.get_template('tv_favorites.html')
	context = RequestContext(request, {
		'fav_list': fav_list,
	})
	return HttpResponse(template.render(context))

@login_required
def show(request, pk):
	show_item = Show.objects.get(pk = pk)
	seasons_list = show_item.season_set.all().order_by('number')
	is_favorite = Show_Favorite.objects.filter(show=show_item,user=request.user,active=True).count() > 0
	banner = ''
	req = urllib2.Request("http://yarrr.me/api/show?id="+show_item.tvdbid, None, {'user-agent':'Chrome/28.0.1500.72'})
	opener = urllib2.build_opener()
	f = opener.open(req)
	showapi = json.load(f)
	banner = showapi[0]['banner']
	template = loader.get_template('tv_show.html')
	context = RequestContext(request, {
		'show': show_item,
		'season_list': seasons_list,
		'show_banner': banner,
		'is_favorite': is_favorite,
	})
	return HttpResponse(template.render(context))

@login_required
def show_use_sickbeard(request, pk):
	show_item = Show.objects.get(pk = pk)
	show_item.use_sickbeard = not show_item.use_sickbeard
	template = loader.get_template('tv_show.html')
	context = RequestContext(request, {
		'show': show_item,
	})
	return HttpResponse(template.render(context))

@login_required
def season(request, pk):
	season_item = Season.objects.get(pk = pk)
	seasons_list = season_item.show.season_set.all().order_by('number')
	episodes_list = season_item.episode_set.all().order_by('number')
	banner = ''
	req = urllib2.Request("http://yarrr.me/api/show?id="+season_item.show.tvdbid, None, {'user-agent':'Chrome/28.0.1500.72'})
	opener = urllib2.build_opener()
	f = opener.open(req)
	showapi = json.load(f)
	banner = showapi[0]['banner']
	template = loader.get_template('tv_season.html')
	context = RequestContext(request, {
		'season': season_item,
		'show': season_item.show,
		'episode_list': episodes_list,
		'season_list': seasons_list,
		'show_banner': banner,
	})
	return HttpResponse(template.render(context))

@login_required
def episode(request, pk):
	episode_item = Episode.objects.get(pk = pk)
	views = Episode_Play.objects.filter(viewer=request.user,episode=episode_item)
	if views.count == 0:
		v = Episode_Play(viewer=request.user,episode=episode_item)
		v.save()
	ip = ""
	if episode_item.location:

		hextime = hex(int(time.time()))[2:]
		file_name = episode_item.location.split(settings.MOD_AUTH_PROTECTED_PATH[:-1])[1]
		md5_hash = hashlib.md5(settings.MOD_AUTH_SECRET+file_name+hextime+request.META['REMOTE_ADDR']).hexdigest()
		protected_url = settings.MOD_AUTH_PROTECTED_URL+md5_hash+'/'+hextime+file_name
	else:
		protected_url = ''
	
	template = loader.get_template('tv_episode.html')
	context = RequestContext(request, {
		'episode': episode_item,
		'protected_url': protected_url,
		'user_ip': request.META['REMOTE_ADDR'],
	})
	return HttpResponse(template.render(context))

@login_required
def episode_update(request, pk):
	episode_item = Episode.objects.get(pk = pk)
	episode_item.info_update=True
	episode_item.save()
	template = loader.get_template('tv_episode.html')
	context = RequestContext(request, {
		'episode': episode_item,
		'protected_url': '',
	})
	return HttpResponse(template.render(context))

@login_required
def search(request):
	searchterm = request.POST['term']
	show_list = Show.objects.filter(Q(name__icontains=searchterm) | Q(description__icontains=searchterm) | Q(genre__icontains=searchterm)).distinct().order_by('name')
	template = loader.get_template('tv_index.html')
	context = RequestContext(request, {
		'show_list': show_list,
	})
	return HttpResponse(template.render(context))

@login_required
def admin_dashboard(request):
	show_list = Show.objects.all()
	season_list = Season.objects.all()
	episode_list = Episode.objects.all()

	episodes_need_update = episode_list.filter(info_update=True)
	episode_views = Episode_Play.objects.all()
	episode_views_last24 = episode_views.filter(date_played__range=(datetime.datetime.now()-timedelta(hours=24), datetime.datetime.now()))

	template = loader.get_template('tv_admin_dashboard.html')
	context = RequestContext(request, {
		'show_count': show_list.count,
		'season_count': season_list.count,
		'episode_count': episode_list.count,
		'episodes_need_update': episodes_need_update.count,
		'episode_views': episode_views.count,
		'episode_views_last24': episode_views_last24.count,
	})
	return HttpResponse(template.render(context))

