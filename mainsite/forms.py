from django.forms import *
from mainsite.models import News
from django.contrib.admin.widgets import AdminDateWidget

class NewsForm(ModelForm):
	date = DateTimeField(widget=AdminDateWidget())
	is_published = BooleanField(help_text="Only published posts will be visible to the outside users. However, it will be visible to administrators like yourself!", required=False)
	
	class Meta:
		model = News