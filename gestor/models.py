from django.db import models
from django.contrib.auth.models import User

#rom django.contrib import admin

# Create your models here.

class Project(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	status = models.BooleanField(default=True)
	manager = models.ForeignKey(User, related_name='id_manager')
	workers = models.ManyToManyField(User, related_name = 'id_worker')
	
	def __unicode__(self):
		return u"%s" % self.name


#admin.site.register(Project)