from django.forms import *
from accounts.models import UserProfile
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _

from accounts.widgets import ImageWidget
from accounts.fields import LimitedImageField

from django.conf import settings

class UserProfileForm(ModelForm):
	user = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	photo = LimitedImageField(widget=ImageWidget(UserProfile), required=False)
	
	class Meta:
		model = UserProfile
	
	def clean(self):
		res = super(UserProfileForm, self).clean()
		print self._errors
		if 'photo' in self._errors:
			self.fields['photo'].widget.instance = self.instance
		
		return res
	
	def save(self, *args, **kwargs):
		if 'photo' in self.changed_data and self.instance and self.instance.photo:
			if not self.instance.photo_is_default():
				self.instance.photo.delete()
		
		resp = super(UserProfileForm, self).save(*args, **kwargs)
		
		if self.data.has_key('remove_pic') and not self.instance.photo_is_default():
			resp.delete_photo()
		
		return resp

class UserProfileAdminForm(UserProfileForm):
	user = ModelChoiceField(queryset=User.objects.all())

class UserForm(UserChangeForm):
	username = CharField(_('username'), help_text=_("30 characters or fewer (letters, digits and underscores). Changing this will change your public curriculum's URL."))
	
	class Meta:
		model = User
		fields = ('username','first_name','last_name','email')
		