from django.db import models
from django.contrib.auth.models import User

import datetime

class News(models.Model):
	""" Website News """
	
	title = models.CharField(max_length=200)
	date = models.DateTimeField()
	body = models.TextField()
	author = models.ForeignKey(User, related_name='news_set', null=True, blank=True, default='')
	
	def save(self):
		if not self.id:
			self.date = datetime.datetime.now()
		super(News, self).save()
	
	def __unicode__(self):
		return u"%s" % self.title
		
	def get_absolute_url(self):
		return u"/noticias/%s/" % self.id
		
	def has_author(self):
		try: self.author
		except: return False
		
		return True
		
	class Meta:
		verbose_name_plural = "news"