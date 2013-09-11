# Create your views here.
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.db.models import Q

from bitsync.models import sync_item, sync_key, sync_link

@login_required
def index(request):
	latest_link_list = sync_link.objects.filter(public = True).order_by('date_added')
	your_link_list = sync_link.objects.filter(Q(allowed_users__username=User)).order_by('date_added')
	template = loader.get_template('index.html')
	context = RequestContext(request, {
		'latest_link_list': latest_link_list,
		'your_link_list': your_link_list,
	})
	return HttpResponse(template.render(context))

@login_required
def link(request, link_id):
	link = sync_link.objects.get(pk=link_id)
	template = loader.get_template('link.html')
	context = RequestContext(request, {
		'link': link,
	})
	return HttpResponse(template.render(context))

@login_required
def item(request, item_id):
	item = sync_item.objects(pk=item_id)
	template = loader.get_template('item.html')
	context = RequestContext(request, {
		'item': item,
	})
	return HttpResponse(template.render(context))

@login_required
def key(request, key_id):
	key = sync_key.objects(pk=key_id)
	template = loader.get_template('key.html')
	context = RequestContext(request, {
		'key': key,
	})
	return HttpResponse(template.render(context))