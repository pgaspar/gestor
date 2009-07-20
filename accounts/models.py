from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	
	user = models.ForeignKey(User, unique=True)
	
	organization = models.CharField("Organization", max_length=20, default='jeKnowledge', null=True)
	title = models.CharField("Position", max_length=40, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	
	class Meta:
		permissions = (('view_profiles', 'View all Profiles'),
					   ('can_search_everything', 'Search Everything'),)
		
	def __unicode__(self):
		return u"%s's Profile" % self.user.get_full_name()
		
	def get_absolute_url(self):
		return "/users/%s/" % self.user.username