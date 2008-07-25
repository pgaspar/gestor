from django.forms import form_for_model, form_for_instance, save_instance, BaseForm, Form, CharField
from gestor.models import Note

NoteForm = form_for_model(Note)