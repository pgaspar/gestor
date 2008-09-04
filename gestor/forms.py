from django.forms import *
from gestor.models import Note, ActionItem, Project, File
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget, AdminFileWidget

import datetime

class NoteForm(ModelForm):
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	project = ModelChoiceField(queryset=Project.objects.all(),widget=HiddenInput())
	description = CharField(widget=Textarea(),help_text="(supports <a href='http://hobix.com/textile/' target='_blank'>textile</a>)")
	class Meta:
		model = Note

class FileForm(ModelForm):
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	project = ModelChoiceField(queryset=Project.objects.all(),widget=HiddenInput())
	content = FileField(widget=AdminFileWidget)
	class Meta:
		model = File	
		
class ActionForm(ModelForm):
	due_date = DateTimeField(widget=AdminDateWidget(),initial=datetime.date.today())
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	project = ModelChoiceField(queryset=Project.objects.all(),widget=HiddenInput())
	description = CharField(widget=Textarea(),help_text="(supports <a href='http://hobix.com/textile/' target='_blank'>textile</a>)")
	class Meta:
		model = ActionItem