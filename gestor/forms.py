from django.forms import *
from gestor.models import Note, ActionItem
from django.contrib.admin.widgets import AdminDateWidget

class NoteForm(ModelForm):
	class Meta:
		model = Note
		
		
class ActionForm(ModelForm):
	due_date = DateTimeField(widget=AdminDateWidget())
	class Meta:
		model = ActionItem