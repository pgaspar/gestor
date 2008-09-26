from django.db import models
from django.core.exceptions import PermissionDenied


class Noticia(models.Model):
	"""(Noticia description)"""
	
	author = models.ForeignKey(User, related_name='news_set')	# not sure about this related_name
	title = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now=True)
	body = models.TextField()
	
	

	class Admin:
		list_display = ('',)
		search_fields = ('',)
		# Textmate's budles ftw, right? :)

	def __unicode__(self):
		return u"%s" % self.title
	
	def isAuthor(self, user):
		if not user is self.author or user.is_staff:
			raise PermissionDenied()	# getting ready for the 'edit news' function. 