from django.contrib import admin
from tv.models import *

admin.site.register(Show)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Episode_Play)