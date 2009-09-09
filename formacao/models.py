from django.db import models
import datetime

class Event(models.Model):
	""" Events (Workshops & Talks) """

	name = models.CharField(max_length=200)
	slug = models.SlugField(default="")
	date = models.DateTimeField()
	
	is_published = models.BooleanField(default=False, help_text="If false, the event isn't displayed to the public.")
	is_short_preview = models.BooleanField(default=False, help_text="If true, does not show any links to the event's page.")
	close_registration = models.BooleanField(default=False, help_text="If true, people won't be able to submit the registration form anymore.")
	
	description = models.TextField(max_length=400)
	details = models.TextField(blank=True, null=True)
	content = models.TextField()
	
	eventType = models.IntegerField(default=1, choices=((1, 'Talk') ,(2, 'Workshop')) )
	
	iframeUrl_surveys = models.CharField(max_length=700, null=True, blank=True, help_text="Event's survey iFrame URL goes here (Example: http://spreadsheets.google.com/embeddedform?key=rturSbnMT6sgthWtfh6OnSw). Redirect the survey here: http://jeknowledge.com/formacao/thanks/")
	iframeUrl_registration = models.CharField(max_length=700, null=True, blank=True, help_text="Same thing as above, except this one is for the registration form. Redirect the survey here: http://jeknowledge.com/formacao/EVENT_ID/confirm/")
	confirmBox = models.TextField(null=True, blank=True, help_text="You should only use this if you have the inscription's iFrame URL.")
	
	privateContent = models.TextField(blank=True, null=True)
	password = models.CharField(max_length=20, null=True, blank=True)
	
	def __unicode__(self):
		return u"%s" % self.name

	def get_absolute_url(self):
		if self.slug != "":
			return u"/formacao/%s/" % self.slug
		else:
			return u"/formacao/%s/" % self.id
		
	def get_private_url(self):
		return u"/formacao/%s/private/" % self.id
	
	def isTalk(self):
		return self.get_eventType_display() == 'Talk'
		
	def isWorkshop(self):
		return self.get_eventType_display() == 'Workshop'