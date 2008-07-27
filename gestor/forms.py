from django.forms import *
from gestor.models import Note, ActionItem, Project
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget

class NoteForm(ModelForm):
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	project = ModelChoiceField(queryset=Project.objects.all(),widget=HiddenInput())
	class Meta:
		model = Note
		
		
class ActionForm(ModelForm):
	due_date = DateTimeField(widget=AdminDateWidget())
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	project = ModelChoiceField(queryset=Project.objects.all(),widget=HiddenInput())
	class Meta:
		model = ActionItem