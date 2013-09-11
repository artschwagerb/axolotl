#!/usr/bin/env python
import os
import sys
import urllib
import urllib2
import json
import datetime

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yarrr.settings")

from tv.models import Show, Season, Episode

from django.core.exceptions import MultipleObjectsReturned			

req = urllib2.Request("http://yarrr.me:9000/api/700dc3d941b692fc440cd3a5cfbe5a92/?cmd=shows", None, {'user-agent':'Chrome/28.0.1500.72'})
opener = urllib2.build_opener()
f = opener.open(req)
showapi = json.load(f)

for s in showapi:
	show_id = s['tvdbid'].encode('utf8')
	print '-----------'
	try:
		update_show = Show.objects.get(tvdbid = show_id)
	
		req = urllib2.Request("http://yarrr.me/api/show?id=" + show_id, None, {'user-agent':'Chrome/28.0.1500.72'})
		opener = urllib2.build_opener()
		f = opener.open(req)
		showapi_detail = json.load(f)
		
		for s in showapi_detail:
			update_show.name=s['show_name'].encode('utf8')[:200]
			update_show.description=s['description'].encode('utf8')
			update_show.date_added=s['date_added'].encode('utf8')
			update_show.date_updated=datetime.date.today()
			update_show.date_aired=s['date_aired'].encode('utf8')
			update_show.file_path=s['filepath'].encode('utf8')[:200]
			update_show.tvdbid=s['tvdb_series_id'].encode('utf8')
			update_show.genre=s['genre'].encode('utf8')[:200]
			update_show.airs_dayofweek=s['airs_dayofweek'].encode('utf8')[:50]
			update_show.airs_time=s['airs_time'].encode('utf8')[:50]
			update_show.content_rating=s['content_rating'].encode('utf8')[:50]
			update_show.network=s['network'].encode('utf8')[:50]
			update_show.actors=s['actors'].encode('utf8')[:400]
			update_show.runtime=s['runtime'].encode('utf8')[:42] + ' minutes'
			update_show.save()

			
		print 'Updated Show - ' + s['name']
	except Show.MultipleObjectsReturned as e:
		new_show = Show.objects.filter(tvdbid = show_id).reverse()[0].delete()
		print 'Deleted Show (Duplicate) - ' + show_id
	except Show.DoesNotExist:
		new_show = Show(
			name=s['name'].encode('utf8'),
			description=s['description'].encode('utf8'),
			date_added=datetime.date.today(),
			date_updated=datetime.date.today(),
			date_aired=datetime.date.today(),
			file_path=s['filepath'].encode('utf8'),
			tvdbid=s['tvdb_series_id'].encode('utf8'),
			genre="",
			airs_dayofweek="",
			airs_time="",
			content_rating="",
			network="",
			actors="",
			runtime="",	
		)
		new_show.save()
		print 'Created Show - ' + s['name']
	except ValidationError:
		print 'Error Processing Show: ' + s['name']
