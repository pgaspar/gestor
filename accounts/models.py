from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail.fields import ImageWithThumbnailsField

from django.conf import settings

class UserProfile(models.Model):
	
	user = models.ForeignKey(User, unique=True)
	
	im = models.CharField("IM", max_length=40, blank=True, null=True)
	
	organization = models.CharField("Organization", max_length=20, default='jeKnowledge', null=True)
	title = models.CharField("Position", max_length=40, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	
	photo = ImageWithThumbnailsField(
		upload_to="photos",
		default=settings.DEFAULT_AVATAR,
		thumbnail={'size':(80,80)},
		extra_thumbnails={
			'small': {'size':(40,40)},
		},
	)
	
	class Meta:
		permissions = (('view_profiles', 'View all Profiles'),
					   ('can_search_everything', 'Search Everything'),)
		
	def __unicode__(self):
		return u"%s's Profile" % self.user.get_full_name()
		
	def get_absolute_url(self):
		return "/users/%s/" % self.user.username
		
	def photo_is_default(self):
		return self.photo == settings.DEFAULT_AVATAR
	
	def delete_photo(self):
		self.photo.delete()
		self.photo = settings.DEFAULT_AVATAR
		self.save()