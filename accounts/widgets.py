from django.forms import *
from gestor.models import *

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from django.conf import settings

# Admin Image widget override that adds a "remove file" checkbox
class ImageWidget(AdminFileWidget):
	def render(self, name, value, attrs=None):
		output = []
		if value: output.append('<a target="_blank" href="%s">%s</a><br />%s <a target="_blank" href="%s">%s</a><br />%s ' % \
					(value.url, value.extra_thumbnails_tag['small'], _('Currently:'), value.url, value, _('Change:')))
					
		output.append(super(AdminFileWidget, self).render(name, value, attrs))
		
		if value and hasattr(value, "url") and value != settings.DEFAULT_AVATAR:
			output.append(u'<br />%s <input type="checkbox" name="remove_pic" value="check" />' %(_(u'Remove:')))
		
		return mark_safe(u''.join(output))
