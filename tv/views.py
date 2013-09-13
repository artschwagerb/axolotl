# Create your views here.
import urllib2
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import timezone

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
def show(request, pk):
	show_item = Show.objects.get(pk = pk)
	seasons_list = show_item.season_set.all().order_by('number')
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
	})
	return HttpResponse(template.render(context))

@login_required
def season(request, pk):
	season_item = Season.objects.get(pk = pk)
	seasons_list = season_item.show.season_set.all()
	episodes_list = season_item.episode_set.all()
	template = loader.get_template('tv_season.html')
	context = RequestContext(request, {
		'season': season_item,
		'show': season_item.show,
		'episode_list': episodes_list,
		'season_list': seasons_list,
	})
	return HttpResponse(template.render(context))

@login_required
def episode(request, pk):
	episode_item = Episode.objects.get(pk = pk)
	v = Viewed(viewer=request.user,date_added=timezone.now())
	v.save()
	episode_item.views.add(v)
	template = loader.get_template('tv_episode.html')
	context = RequestContext(request, {
		'episode': episode_item,
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

