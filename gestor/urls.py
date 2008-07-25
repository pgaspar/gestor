from django.conf.urls.defaults import *
from gestor.models import Project, Note, ActionItem


urlpatterns = patterns('',
    (r'^$', 'gestor.views.project_list',),
	(r'^project/(?P<object_id>\d+)/$', 'gestor.views.project_detail', ),
	
	(r'^action/(?P<object_id>\d+)/$', 'gestor.views.action_detail', ),
	
	(r'^note/(?P<object_id>\d+)/$', 'gestor.views.note_detail', ),
	(r'^note/new/$', 'django.views.generic.create_update.create_object', { 'model': Note, 'login_required':True, 'template_name':'note_edit.html' } ),
	(r'^note/(?P<object_id>\d+)/edit/$', 'django.views.generic.create_update.update_object', { 'model': Note, 'login_required':True, 'template_name':'note_edit.html' } ),
	(r'^note/(?P<object_id>\d+)/delete/$', 'note_delete', ),
)
