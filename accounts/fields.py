from django.forms import *
from gestor.models import *
from django.utils.translation import ugettext as _

# ImageField that validates the image's size
class LimitedImageField(ImageField):
	
	def __init__(self, max_size = 1, *args, **kwargs):
		self.max_size = max_size
		super(LimitedImageField, self).__init__(*args, **kwargs)
		
	def clean(self, value, initial):
		result = super(LimitedImageField, self).clean(value, initial)
		
		if result and result.size > self.max_size * 1024 * 1024:
			raise ValidationError(_(u'The image is too big. Max size is 1MB.'))
		
		return result
		
		
