from django.conf.urls.defaults import *
from gestor.models import Project, Note, ActionItem

from gestor.forms import NoteForm, ActionForm

from gestor.feeds import ActionItemFeed

feeds = {
    'ActionItems': ActionItemFeed,
}


urlpatterns = patterns('',
    (r'^$', 'gestor.views.project_list',),
	(r'^project/(?P<object_id>\d+)/$', 'gestor.views.project_detail', ),
	
	
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
	
	(r'^action/(?P<object_id>\d+)/$', 'gestor.views.action_detail', ),
	(r'^action/in/(?P<object_id>\d+)/$', 'gestor.views.action_create', ),
	(r'^action/(?P<object_id>\d+)/edit/$', 'gestor.views.action_edit',),
	(r'^action/(?P<object_id>\d+)/delete/$', 'gestor.views.action_delete',),
	(r'^action/(?P<object_id>\d+)/finish/$', 'gestor.views.action_finish', ),

	
	(r'^note/(?P<object_id>\d+)/$', 'gestor.views.note_detail', ),
	(r'^note/in/(?P<object_id>\d+)/$', 'gestor.views.note_create', ),
	(r'^note/(?P<object_id>\d+)/edit/$', 'gestor.views.note_edit',),
	(r'^note/(?P<object_id>\d+)/delete/$', 'gestor.views.note_delete',),

	(r'^file/(?P<object_id>\d+)/$', 'gestor.views.file_detail', ),
	(r'^file/in/(?P<object_id>\d+)/$', 'gestor.views.file_create', ),
	(r'^file/(?P<object_id>\d+)/edit/$', 'gestor.views.file_edit',),
	(r'^file/(?P<object_id>\d+)/delete/$', 'gestor.views.file_delete',),

)
