from django.db import models
import datetime

class Event(models.Model):
	""" Events (Workshops & Talks) """

	name = models.CharField(max_length=200)
	date = models.DateTimeField()
	is_published = models.BooleanField(default=False)
	
	description = models.TextField(max_length=400)
	details = models.TextField(blank=True, null=True)
	content = models.TextField()
	
	eventType = models.IntegerField(default=1, choices=((1, 'Talk') ,(2, 'Workshop')) )
	
	privateContent = models.TextField(blank=True, null=True)
	password = models.CharField(max_length=20, null=True, blank=True)
	
	def __unicode__(self):
		return u"%s" % self.name

	def get_absolute_url(self):
		return u"/formacao/%s/" % self.id
		
	def get_private_url(self):
		return u"/formacao/%s/private/" % self.id
	
	def isTalk(self):
		return self.get_eventType_display() == 'Talk'