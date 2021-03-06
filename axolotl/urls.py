from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	url(r'^$', 'axolotl.views.home', name='home'),
	# url(r'^axolotl/', include('axolotl.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
	#(r'^accounts/', include('invitation.urls')),
	#url(r'^accounts/', include('registration.backends.default.urls')),
	url(r'^accounts/profile/', 'axolotl.views.profile', name='profile'),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {
			'template_name': 'login.html'
	}, name="login"),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login',
		name="logout"),

	url(r'^bitsync/', include('bitsync.urls')),
	url(r'^tv/', include('tv.urls')),

)
