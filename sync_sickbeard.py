#!/usr/bin/env python
import os
import sys
import urllib
import urllib2
import json
import datetime
from datetime import datetime
from django.conf import settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "axolotl.local_settings")

from tv.models import Show, Season, Episode

from django.core.exceptions import MultipleObjectsReturned			

#list all shows
req = urllib2.Request(settings.SICKBEARD_API_URL+"?cmd=shows", None, {'user-agent':'Chrome/28.0.1500.72'})
opener = urllib2.build_opener()
f = opener.open(req)
showapi = json.load(f)

#loop shows
for slink in showapi["data"]:
	show_id = slink
	print ''
	print '-----------'
	print ''
	print 'tvdbid: ' + show_id
	#get show details
	req = urllib2.Request(settings.SICKBEARD_API_URL+"?cmd=show&tvdbid=" + show_id, None, {'user-agent':'Chrome/28.0.1500.72'})
	opener = urllib2.build_opener()
	f = opener.open(req)
	showapi_detail = json.load(f)

	if not showapi_detail["result"] == "success":
		continue
	
	#loop show details
	try:
		update_show = Show.objects.get(tvdbid = show_id)

		if not update_show.name:
			update_show.name=showapi_detail["data"]['show_name'].encode('utf8')[:200]

		#update_show.date_added=showapi_detail["data"]['date_added'].encode('utf8')
		#update_show.date_updated=datetime.date.today()
		#update_show.date_aired=showapi_detail["data"]['date_aired'].encode('utf8')
		if showapi_detail["data"]['next_ep_airdate']:
			update_show.date_next_episode=datetime.strptime(showapi_detail["data"]['next_ep_airdate'].encode('utf8'), "%Y-%m-%d")

		if not update_show.file_path:
			update_show.file_path=showapi_detail["data"]['location'].encode('utf8')

		#update_show.tvdbid=showapi_detail["data"]['tvdb_series_id'].encode('utf8')

		if not update_show.genre:
			update_show.genre=",".join(showapi_detail["data"]['genre']).encode('utf8')[:200]

		if not update_show.airs:
			update_show.airs=showapi_detail["data"]['airs'].encode('utf8')[:50]

		update_show.network=showapi_detail["data"]['network'].encode('utf8')[:50]
		#update_show.actors=showapi_detail["data"]['actors'].encode('utf8')[:400]
		#update_show.runtime=showapi_detail["data"]['runtime'].encode('utf8')[:42] + ' minutes'
		update_show.save()

			
		print 'Updated Show - ' + showapi_detail["data"]['show_name']
	except Show.MultipleObjectsReturned as e:
		new_show = Show.objects.filter(tvdbid = show_id).reverse()[0].delete()
		print 'Deleted Show (Duplicate) - ' + show_id
	except Show.DoesNotExist:
		#print showapi_detail["data"]["show_name"]
		new_show = Show(
			name=showapi_detail["data"]['show_name'].encode('utf8')[:200],
			date_next_episode=datetime.strptime(showapi_detail["data"]['next_ep_airdate'].encode('utf8'), "%Y-%m-%d"),
			file_path=showapi_detail["data"]['location'].encode('utf8'),
			genre=",".join(showapi_detail["data"]['genre']).encode('utf8')[:200],
			tvdbid=show_id.encode('utf8'),
			airs=showapi_detail["data"]['airs'].encode('utf8')[:50],
			network=showapi_detail["data"]['network'].encode('utf8')[:50],
		)
		new_show.save()
		print 'Created Show - ' + showapi_detail["data"]['show_name']