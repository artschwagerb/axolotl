import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# Create your models here.
class Viewed(models.Model):
    viewer = models.ForeignKey(User)
    date_added = models.DateTimeField('date_added',auto_now_add=True, editable=False,blank=True,null=True)
    def __unicode__(self):
        return u'%s - %s' % (self.viewer.username, self.date_added)
class Show(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_added = models.DateTimeField('date_added',auto_now_add=True, editable=False,blank=True,null=True)
    date_updated = models.DateTimeField('date_updated',auto_now_add=True, auto_now=True, editable=False,blank=True,null=True)
    date_aired = models.DateTimeField('date_aired')
    file_path = models.CharField(max_length=200)
    tvdbid = models.IntegerField()
    genre = models.CharField(max_length=200)
    airs_dayofweek = models.CharField(max_length=10)
    airs_time = models.CharField(max_length=10)
    content_rating = models.CharField(max_length=10)
    network = models.CharField(max_length=25)
    actors = models.CharField(max_length=200)
    runtime = models.CharField(max_length=25)
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.tvdbid)
    def updated_recently(self):
        return self.date_updated >= timezone.now() - datetime.timedelta(days=3)
    class Meta:
        ordering = ['name']
class Season(models.Model):
    show = models.ForeignKey(Show)
    number = models.IntegerField()
    date_added = models.DateTimeField('date_added',auto_now_add=True, editable=False,blank=True,null=True)
    date_updated = models.DateTimeField('date_updated',auto_now_add=True, auto_now=True, editable=False,blank=True,null=True)
    date_aired = models.DateTimeField('date aired')
    season_tvdbid = models.IntegerField()
    def __unicode__(self):
        return u'%s - S%s (%s)' % (self.show.name, self.number, self.season_tvdbid)

class Episode(models.Model):
    season = models.ForeignKey(Season)
    show = models.ForeignKey(Show)
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    description = models.TextField()
    hits = models.IntegerField()
    date_added = models.DateTimeField('date_added',auto_now_add=True, editable=False,blank=True,null=True)
    date_updated = models.DateTimeField('date_updated',auto_now_add=True, auto_now=True, editable=False,blank=True,null=True)
    date_aired = models.DateTimeField('date aired')
    rating = models.CharField(max_length=10)
    episode_tvdbid = models.IntegerField()
    views = models.ManyToManyField(Viewed)
    def __unicode__(self):
        return u'%s - S%sE%s %s (%s)' % (self.show.name, self.season.number, self.number, self.name, self.episode_tvdbid)
