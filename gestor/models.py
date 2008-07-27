from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Project(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	active = models.BooleanField(default=True)
	manager = models.ForeignKey(User, related_name='projects_managed')
	team = models.ManyToManyField(User, related_name = 'projects_working')
	start_date = models.DateField()
	end_date = models.DateField()
	
	def __unicode__(self):
		return u"%s" % self.name
		
		
	def get_absolute_url(self):
		return "/gestor/project/%d" % self.id


class ActionItem(models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)
	author = models.ForeignKey(User, related_name='actionitem_set')
	targets = models.ManyToManyField(User, related_name = 'actionitem_todo')
	set_date = models.DateField(auto_now_add=True)
	due_date = models.DateField(blank=True, null=True)
	done = models.BooleanField(default=False)

	
	def __unicode__(self):
		return u"%s" % self.title
	
	def get_absolute_url(self):
		return "/gestor/action/%s" % self.id 

class Note(models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)
	author = models.ForeignKey(User)
	set_date = models.DateField(auto_now_add=True)

	def __unicode__(self):
		return u"%s" % self.title
	
	def get_absolute_url(self):
		return "/gestor/note/%s" % self.id