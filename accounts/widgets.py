from django.forms import *
from gestor.models import *

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from accounts.utils import thumbnail
from django.conf import settings

# Admin Image widget override that adds a "remove file" checkbox
class ImageWidget(AdminFileWidget):
	def __init__(self, model = None, *args, **kwargs):
		super(ImageWidget, self).__init__(*args, **kwargs)
		self.model = model
		
	def render(self, name, value, attrs=None):
		output = []
		
		if (value and hasattr(value, 'url')) or (value and 'instance' in vars(self)):
			if not hasattr(value, 'url'): value = self.instance.photo
			output.append('<table style="border: 0px;"><tr><td style="vertical-align: middle; border: 0px;"><a target="_blank" href="%s">%s</a></td><td style="vertical-align: middle; border: 0px;">%s <a target="_blank" href="%s">%s</a><br />%s ' % \
				(value.url, value.extra_thumbnails_tag['small'], _('Currently:'), value.url, value, _('Change:')))
		else:
			file_path = settings.MEDIA_URL + settings.DEFAULT_AVATAR
			output.append('<table style="border: 0px;"><tr><td style="vertical-align: middle; border: 0px;"><a target="_blank" href="%s">%s</a></td><td style="vertical-align: middle; border: 0px;">%s <a target="_blank" href="%s">%s</a><br />%s ' % \
				(file_path, thumbnail(settings.DEFAULT_AVATAR, (40,40)), _('Currently:'), file_path, settings.DEFAULT_AVATAR, _('Change:')))
		
		output.append(super(AdminFileWidget, self).render(name, value, attrs))
		
		if value and hasattr(value, "url") and value != settings.DEFAULT_AVATAR:
			output.append(u'<br />%s <input type="checkbox" name="remove_pic" value="check" />' %(_(u'Remove:')))
		
		output.append(u'</td></tr></table>')
		return mark_safe(u''.join(output))
