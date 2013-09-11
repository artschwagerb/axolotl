from django.http import HttpResponse
from django.template import RequestContext, loader

from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
		template = loader.get_template('home.html')
		context = RequestContext(request, {
			#'latest_post_list': latest_post_list,
		})
		return HttpResponse(template.render(context))

@login_required
def profile(request):
		template = loader.get_template('profile.html')
		context = RequestContext(request, {

		})
		return HttpResponse(template.render(context))