import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# Create your models here.
class Show(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(null=True,blank=True)
	date_added = models.DateTimeField('date_added',auto_now_add=True, editable=False,blank=True,null=True)
	date_updated = models.DateTimeField('date_updated',auto_now_add=True, auto_now=True, editable=False,blank=True,null=True)
	date_aired = models.DateTimeField('date_aired',null=True,blank=True)
	date_next_episode = models.DateTimeField('date_next_episode',null=True,blank=True)
	file_path = models.CharField(max_length=200,null=True,blank=True)
	tvdbid = models.CharField(max_length=10,null=True,blank=True)
	genre = models.CharField(max_length=200,null=True,blank=True)
	status = models.CharField(max_length=25,null=True,blank=True)
	airs = models.CharField(max_length=25,null=True,blank=True)
	content_rating = models.CharField(max_length=25,null=True,blank=True)
	network = models.CharField(max_length=25,null=True,blank=True)
	actors = models.CharField(max_length=200,null=True,blank=True)
	runtime = models.CharField(max_length=25,null=True,blank=True)
	use_sickbeard = models.BooleanField(default=True)
	def __unicode__(self):
		return u'%s (%s)' % (self.name, self.tvdbid)
	def updated_recently(self):
		return self.date_updated >= timezone.now() - datetime.timedelta(days=3)
	def genre_list(self):
		return self.genre.split(',')
	class Meta:
		verbose_name_plural = "shows"
		ordering = ['name']
		permissions = (("can_view_shows", "Can view shows"),)

class Season(models.Model):
	show = models.ForeignKey(Show)
	number = models.IntegerField(default=0,null=True,blank=True)
	date_added = models.DateTimeField('date_added',auto_now_add=True, editable=False,blank=True,null=True)
	date_updated = models.DateTimeField('date_updated',auto_now_add=True, auto_now=True, editable=False,blank=True,null=True)
	date_aired = models.DateTimeField('date aired',null=True,blank=True)
	tvdbid = models.CharField(max_length=10,null=True,blank=True)
	def __unicode__(self):
		return u'%s - S%s (%s)' % (self.show.name, self.number, self.tvdbid)
	class Meta:
		verbose_name_plural = "seasons"

class Episode(models.Model):
	season = models.ForeignKey(Season)
	show = models.ForeignKey(Show)
	name = models.CharField(max_length=200)
	number = models.IntegerField(default=0,null=True,blank=True)
	description = models.TextField(null=True,blank=True)
	hits = models.IntegerField(default=0,null=True,blank=True,editable=False)
	date_added = models.DateTimeField('date_added',auto_now_add=True, editable=False,blank=True,null=True)
	date_updated = models.DateTimeField('date_updated',auto_now_add=True, auto_now=True, editable=False,blank=True,null=True)
	date_aired = models.DateTimeField('date aired',null=True,blank=True)
	rating = models.CharField(max_length=10,null=True,blank=True)
	tvdbid = models.CharField(max_length=10,null=True,blank=True)
	status = models.CharField(max_length=25,null=True,blank=True,editable=False)
	location = models.CharField(max_length=250,null=True,blank=True)
	file_size = models.CharField(max_length=10,null=True,blank=True,editable=False)
	file_exists = models.BooleanField(default=False)
	info_update = models.BooleanField(default=False)
	def __unicode__(self):
		return u'%s - S%sE%s %s' % (self.show.name, self.season.number, self.number, self.name)
	class Meta:
		verbose_name_plural = "episodes"
		permissions = (("can_play_episodes", "Can play episodes"),)

class Episode_Play(models.Model):
	viewer = models.ForeignKey(User)
	episode = models.ForeignKey(Episode)
	date_played = models.DateTimeField('date_played',auto_now_add=True, editable=False,blank=True,null=True)
	def __unicode__(self):
		return u'%s - %s' % (self.viewer.username, self.date_played)
	class Meta:
		verbose_name_plural = "plays"