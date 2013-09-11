from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class sync_item(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	external_url = models.CharField(max_length=512)
	date_added = models.DateTimeField('date_added',auto_now_add=True, editable=False)
	date_updated = models.DateTimeField('date_updated',auto_now_add=True, auto_now=True, editable=False)
	date_expiration = models.DateTimeField('date_expiration')
	owner = models.ForeignKey(User)
	def __unicode__(self):
		return u'%s (%s) by %s' % (self.name, self.description[:100], self.owner.username)
	def expired(self):
		return self.date_added < timezone.now()
	def added_recently(self):
		return self.date_added >= timezone.now() - datetime.timedelta(days=3)	
	def updated_recently(self):
		return self.date_updated >= timezone.now() - datetime.timedelta(days=3)
	class Meta:
		ordering = ['date_added']
class sync_key(models.Model):
	key = models.CharField(max_length=64)
	date_added = models.DateTimeField('date_added',auto_now_add=True, editable=False)
	date_updated = models.DateTimeField('date_updated',auto_now_add=True, auto_now=True, editable=False)
	date_expiration = models.DateTimeField('date_expiration')
	single_use = models.BooleanField()
	full_access = models.BooleanField()
	def __unicode__(self):
		return u'%s (%s)' % (self.key, self.single_use)
	def expired(self):
		return self.date_expiration < timezone.now()
	def added_recently(self):
		return self.date_added >= timezone.now() - datetime.timedelta(days=3)	
	def updated_recently(self):
		return self.date_updated >= timezone.now() - datetime.timedelta(days=3)
	class Meta:
		ordering = ['date_added']
class sync_link(models.Model):
	item = models.ForeignKey(sync_item)
	key = models.ForeignKey(sync_key)
	date_added = models.DateTimeField('date_added',auto_now_add=True, editable=False)
	date_updated = models.DateTimeField('date_updated',auto_now_add=True, auto_now=True, editable=False)
	date_expiration = models.DateTimeField('date_expiration')
	public = models.BooleanField()
	allowed_users = models.ManyToManyField(User, related_name='users', null=True, blank=True)
	def __unicode__(self):
		return u'%s' % (self.item.name)
	def viewable(self):
		return (self.public == True) or (User in self.allowed_users.all)
	def expired(self):
		return self.date_added < timezone.now()
	def added_recently(self):
		return self.date_added >= timezone.now() - datetime.timedelta(days=3)	
	def updated_recently(self):
		return self.date_updated >= timezone.now() - datetime.timedelta(days=3)
	def owner(self):
		return self.item.owner
	def name(self):
		return self.item.name