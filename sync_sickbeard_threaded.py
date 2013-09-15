#!/usr/bin/env python
import os
import sys
import requests
import json
import datetime
import time
from datetime import datetime

import Queue
import threading
import traceback

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "axolotl.local_settings")

from django.conf import settings

from tv.models import Show, Season, Episode

from django.core.exceptions import MultipleObjectsReturned		

#Functions
#------------------------------

def check_episodes(show_item, season_item):
	headers = {'content-type': 'application/json'}
	payload = {'cmd': 'show.seasons', 'tvdbid': show_item.tvdbid, 'season': season_item.number}
	r = requests.get(sickbeard_api_url, params=payload)

	episodeapi = r.json()

	for epi in episodeapi["data"]:
		try:
			#print episodeapi["data"][epi]["name"]
			update_episode = Episode.objects.get(show=show_item,season=season_item,number=epi)

			if update_episode.info_update:
				headers = {'content-type': 'application/json'}
				payload = {'cmd': 'episode', 'tvdbid': show_item.tvdbid, 'season': season_item.number, 'episode': str(epi)}
				r = requests.get(sickbeard_api_url, params=payload)

				episode_detail_api = r.json()

				update_episode.name=episode_detail_api["data"]["name"].encode('utf8', 'replace')
				update_episode.description=episode_detail_api["data"]["description"].encode('utf8', 'replace')
				update_episode.date_aired=datetime.strptime(episode_detail_api["data"]["airdate"].encode('utf8', 'replace'), "%Y-%m-%d")
				update_episode.location=episode_detail_api["data"]["location"].encode('utf8', 'replace')
				update_episode.file_size=episode_detail_api["data"]["file_size"].encode('utf8', 'replace')
				update_episode.status=episode_detail_api["data"]["status"].encode('utf8', 'replace')
				update_episode.info_update=false

				update_episode.save()
				print "{:3d}  {:40s} {:10s} {:25s}".format(id, show_item.name, "UPDATED EP", 'S'+str(season_item.number)+'E'+str(update_episode.number))
		except Episode.DoesNotExist:
			new_episode = Episode(
				season=season_item,
				show=show_item,
				name=episodeapi["data"][epi]["name"].encode('utf8', 'replace'),
				number=epi,
			)
			new_episode.save()
			print "{:3d}  {:40s} {:10s} {:10}".format(id, show_item.name, "ADDED EP", 'S'+str(season_item.number)+'E'+str(epi))
			#print '	 -Added Episode: '+show_item.name+' - S'+str(season_item.number)+'E'+str(epi)
		except:
			traceback.print_exc()

def check_show(id,show_id):
	try:
		show_startTime = datetime.now()

		headers = {'content-type': 'application/json'}
		payload = {'cmd': 'show', 'tvdbid': show_id}
		r = requests.get(sickbeard_api_url, params=payload)

		showapi_detail = r.json()

		if not showapi_detail["result"] == "success":
			#q.put("Error: result bad")
			return


		update_show = Show.objects.get(tvdbid = show_id)
		#if update_show.use_sickbeard == False:
			#sickbeard doesnt need to check this
		#	return
		#print "{:3d}  {:40s} {:10s}".format(id, update_show.name, "CHECKING")
		#print 'Checking Show #'+id+' - ' + update_show.name

		update_show.name=showapi_detail["data"]['show_name'].encode('utf8', 'replace')[:200]

		#update_show.date_added=showapi_detail["data"]['date_added'].encode('utf8', 'replace')
		#update_show.date_updated=datetime.date.today()
		#update_show.date_aired=showapi_detail["data"]['date_aired'].encode('utf8', 'replace')
		if showapi_detail["data"]['next_ep_airdate']:
			update_show.date_next_episode=datetime.strptime(showapi_detail["data"]['next_ep_airdate'].encode('utf8', 'replace'), "%Y-%m-%d")

		update_show.file_path=showapi_detail["data"]['location'].encode('utf8', 'replace')

		#update_show.tvdbid=showapi_detail["data"]['tvdb_series_id'].encode('utf8', 'replace')

		update_show.genre=",".join(showapi_detail["data"]['genre']).encode('utf8', 'replace')[:200]

		update_show.airs=showapi_detail["data"]['airs'].encode('utf8', 'replace')[:50]

		update_show.network=showapi_detail["data"]['network'].encode('utf8', 'replace')[:50]
		#update_show.actors=showapi_detail["data"]['actors'].encode('utf8', 'replace')[:400]
		#update_show.runtime=showapi_detail["data"]['runtime'].encode('utf8', 'replace')[:42] + ' minutes'

		update_show.save()

		for sea in showapi_detail["data"]['season_list']:
			try:
				update_season = Season.objects.get(show=update_show,number=sea)
				#print '		-Updated Season '+str(sea)
				check_episodes(update_show,update_season)
			except Season.DoesNotExist:
				new_season = Season(
					show=update_show,
					number=sea,
				)
				new_season.save()
				print "{:3d}  {:40s} {:10s} {:3s}".format(id, update_show.name, "ADDED SEA", 'S'+str(sea))
				#print '	 -Added Season - '+update_show.name+' '+str(sea)

		print "{:3d}  {:40s} {:10s} {:25s}".format(id, update_show.name, "UPDATED", str(datetime.now()-show_startTime))
		#print '%d %10s - %s (%s)' % id, "UPDATED", update_show.name, str(datetime.now()-show_startTime)
		#q.put('Updated Show - ' + update_show.name)
	except Show.DoesNotExist:
		#print showapi_detail["data"]["show_name"]
		new_show = Show(
			name=showapi_detail["data"]['show_name'].encode('utf8', 'replace')[:200],
			date_next_episode=datetime.strptime(showapi_detail["data"]['next_ep_airdate'].encode('utf8', 'replace'), "%Y-%m-%d"),
			file_path=showapi_detail["data"]['location'].encode('utf8', 'replace'),
			genre=",".join(showapi_detail["data"]['genre']).encode('utf8', 'replace')[:200],
			tvdbid=show_id.encode('utf8', 'replace'),
			airs=showapi_detail["data"]['airs'].encode('utf8', 'replace')[:50],
			network=showapi_detail["data"]['network'].encode('utf8', 'replace')[:50],
		)
		new_show.save()
		#print '%d %10s - %s' % id, "CREATED", showapi_detail["data"]['show_name']
		print "{:3d}  {:40s} {:10s}".format(id, showapi_detail["data"]['show_name'], "CREATED")
	except:
		print '!!!!!!! ERROR Show #'+str(id)+' - ' + showapi_detail["data"]['show_name']
		traceback.print_exc()



#Operations
#------------------------------


#list all shows
try:
	startTime = datetime.now()

	#create aickbeard url from variables
	if settings.SICKBEARD_URL_PORT:
		sickbeard_api_url = settings.SICKBEARD_URL+":"+settings.SICKBEARD_URL_PORT+"/api/"+settings.SICKBEARD_API_KEY+"/"
	else:
		sickbeard_api_url = settings.SICKBEARD_URL+"/api/"+settings.SICKBEARD_API_KEY+"/"

	#pass in parameters
	payload = {'cmd': 'shows'}

	#get json response
	r = requests.get(sickbeard_api_url, params=payload)

	#save json response to variable
	showapi = r.json()

	#create queue
	q = Queue.Queue()

	#loop shows
	id = 0
	for slink in showapi["data"]:
		id = id + 1
		#print 'Added '+slink+' to the Update ThreadPool'
		#print 'tvdbid: ' + show_id
		#create thread to get show details
		


		t = threading.Thread(target=check_show, args = (id,slink))
		t.daemon = True
		t.start()

		while threading.activeCount() > 9:
			#print '### Waiting 5 seconds for an open Thread...'
			time.sleep(5)

	#s = q.get()
	#print s
	print 'Running Time: '+str(datetime.now()-startTime)
except:
	traceback.print_exc()