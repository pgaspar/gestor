from django.forms import *
from gestor.models import Note, ActionItem, Project, ActionNote, File
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget, AdminFileWidget

import datetime


class CommonForm(ModelForm):
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	project = ModelChoiceField(queryset=Project.objects.all(),widget=HiddenInput())
	notification = BooleanField(help_text=" (Sends email to project members)",required=False)

class NoteForm(CommonForm):
		
	class Meta:
		model = Note

class ActionNoteForm(ModelForm):
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	actionitem = ModelChoiceField(queryset=ActionItem.objects.all(),widget=HiddenInput())
	notification = BooleanField(help_text=" (Sends email to action item team)",required=False)
	
	class Meta:
		model = ActionNote
		
class FileForm(CommonForm):
	content = FileField(widget=AdminFileWidget)
	class Meta:
		model = File	
		
class ActionForm(CommonForm):
	due_date = DateTimeField(widget=AdminDateWidget())
	
	class Meta:
		model = ActionItem
	
class ProjectForm(ModelForm):
	start_date = DateTimeField(widget=AdminDateWidget())
	end_date = DateTimeField(widget=AdminDateWidget())
	
	class Meta:
		model = Project
		
class SearchForm(Form):
	find = CharField(label="Looking for:")