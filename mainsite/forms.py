from django.forms import *
from mainsite.models import News
from django.contrib.admin.widgets import AdminDateWidget

class NewsForm(ModelForm):
	body = CharField(widget=Textarea(),help_text="(supports <a href='http://hobix.com/textile/' target='_blank'>textile</a>)")
	date = DateTimeField(widget=AdminDateWidget())
	is_published = BooleanField(help_text="Only published posts will be visible to the outside users. However, it will be visible to administrators like yourself!")
	
	class Meta:
		model = News