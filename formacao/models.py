from django.db import models
import datetime

class Event(models.Model):
	""" Events (Workshops & Talks) """

	name = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)
	
	content = models.TextField()
	privateContent = models.TextField()
	description = models.TextField(max_length=400)
	details = models.TextField()
	
	type = models.IntegerField(default=1, choices=((1, 'Talk') ,(2, 'Workshop')) )
	password = models.TextField(max_length=20, null=True)
	
	is_published = models.BooleanField(default=False)
	
	def __unicode__(self):
		return u"%s" % self.name

	def get_absolute_url(self):
		return u"/formacao/%s/" % self.id
	