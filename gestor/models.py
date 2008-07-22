from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	status = models.BooleanField(default=True)
	manager = models.ForeignKey(User, related_name='id_manager')
	workers = models.ManyToManyField(User, related_name = 'id_worker')
	start_date = models.DateField()
	end_date = models.DateField()
	
	def __unicode__(self):
		return u"%s" % self.name
		
		
	def get_absolute_url(self):
		return "/gestor/project/%d" % self.id

