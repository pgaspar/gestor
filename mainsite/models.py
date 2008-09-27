from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
	""" Website News """
	
	title = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now=True)
	body = models.TextField()
	
	def __unicode__(self):
		return u"%s" % self.title
		
	def get_absolute_url(self):
		return u"/noticias/%s/" % self.id