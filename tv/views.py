# Create your views here.
import urllib2
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import timezone

from tv.models import Show, Season, Viewed, Episode

@login_required
def index(request):
	latest_show_list = Show.objects.order_by('name')
	template = loader.get_template('tv_index.html')
	context = RequestContext(request, {
		'latest_show_list': latest_show_list,
	})
	return HttpResponse(template.render(context))

@login_required
def show(request, show_id):
	show_item = Show.objects.get(tvdbid = show_id)
	seasons_list = show_item.season_set.all()
	banner = ''
	req = urllib2.Request("http://yarrr.me/api/show?id="+show_id, None, {'user-agent':'Chrome/28.0.1500.72'})
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
def season(request, season_id):
	season_item = Season.objects.get(season_tvdbid = season_id)
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
def episode(request, episode_id):
	episode_item = Episode.objects.get(episode_tvdbid = episode_id)
	v = Viewed(viewer=request.user,date_added=timezone.now())
	v.save()
	episode_item.views.add(v)
	template = loader.get_template('tv_episode.html')
	context = RequestContext(request, {
		'episode': episode_item,
	})
	return HttpResponse(template.render(context))
