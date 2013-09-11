from django.contrib import admin
from tv.models import Show
from tv.models import Season
from tv.models import Episode
from tv.models import Viewed

admin.site.register(Show)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Viewed)