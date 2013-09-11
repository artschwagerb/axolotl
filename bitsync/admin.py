from django.contrib import admin
from bitsync.models import sync_item
from bitsync.models import sync_key
from bitsync.models import sync_link

admin.site.register(sync_item)
admin.site.register(sync_key)
admin.site.register(sync_link)