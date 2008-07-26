from django.conf.urls.defaults import *
from gestor.models import Project, Note, ActionItem

from gestor.forms import NoteForm, ActionForm


urlpatterns = patterns('',
    (r'^$', 'gestor.views.project_list',),
	(r'^project/(?P<object_id>\d+)/$', 'gestor.views.project_detail', ),
	
	(r'^action/(?P<object_id>\d+)/$', 'gestor.views.action_detail', ),
	(r'^action/in/(?P<object_id>\d+)/$', 'gestor.views.action_create', ),
	(r'^action/(?P<object_id>\d+)/edit/$', 'gestor.views.action_edit',),
	(r'^action/(?P<object_id>\d+)/delete/$', 'gestor.views.action_delete',),
	(r'^action/(?P<object_id>\d+)/finish/$', 'gestor.views.action_finish', ),

	
	(r'^note/(?P<object_id>\d+)/$', 'gestor.views.note_detail', ),
	(r'^note/in/(?P<object_id>\d+)/$', 'gestor.views.note_create', ),
	(r'^note/(?P<object_id>\d+)/edit/$', 'gestor.views.note_edit',),
	(r'^note/(?P<object_id>\d+)/delete/$', 'gestor.views.note_delete',),
)
