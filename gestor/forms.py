from django.forms import *
from gestor.models import Note, ActionItem, Project, File
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget, AdminFileWidget


class NoteForm(ModelForm):
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	project = ModelChoiceField(queryset=Project.objects.all(),widget=HiddenInput())
	class Meta:
		model = Note

class FileForm(ModelForm):
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	project = ModelChoiceField(queryset=Project.objects.all(),widget=HiddenInput())
	content = FileField(widget=AdminFileWidget)
	class Meta:
		model = File	
		
class ActionForm(ModelForm):
	due_date = DateTimeField(widget=AdminDateWidget())
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	project = ModelChoiceField(queryset=Project.objects.all(),widget=HiddenInput())
	class Meta:
		model = ActionItem