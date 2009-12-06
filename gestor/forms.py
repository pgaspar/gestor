from django.forms import *
from gestor.models import Note, ActionItem, Project, ActionNote
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget, AdminFileWidget

import datetime


class CommonForm(ModelForm):
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	project = ModelChoiceField(queryset=Project.objects.all(),widget=HiddenInput())
	notification = BooleanField(help_text=" (Sends email to project members)",required=False)

class NoteForm(CommonForm):
	description = CharField(widget=Textarea(),help_text="(supports <a href='http://hobix.github.com/hobix/textile/' target='_blank'>textile</a>)")	
	class Meta:
		model = Note

class ActionNoteForm(ModelForm):
	author = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
	actionitem = ModelChoiceField(queryset=ActionItem.objects.all(),widget=HiddenInput())
	notification = BooleanField(help_text=" (Sends email to action item team)",required=False)
	
	description = CharField(widget=Textarea(),help_text="(supports <a href='http://hobix.github.com/hobix/textile/' target='_blank'>textile</a>)")	
	class Meta:
		model = ActionNote
				
class ActionForm(CommonForm):
	due_date = DateTimeField(widget=AdminDateWidget())
	description = CharField(widget=Textarea(),help_text="(supports <a href='http://hobix.github.com/hobix/textile/' target='_blank'>textile</a>)")
	class Meta:
		model = ActionItem
	
class ProjectForm(ModelForm):
	description = CharField(widget=Textarea(),help_text="(supports <a href='http://hobix.github.com/hobix/textile/' target='_blank'>textile</a>)")
	
	start_date = DateTimeField(widget=AdminDateWidget())
	end_date = DateTimeField(widget=AdminDateWidget())
	
	team = ModelMultipleChoiceField(queryset=User.objects.all().order_by('username'))
	
	class Meta:
		model = Project
		
class SearchForm(Form):
	find = CharField(label="Looking for:")