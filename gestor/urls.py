from django.conf.urls.defaults import *
from gestor.models import Project, Note, ActionItem
from activitystream.models import Activity

from gestor.forms import NoteForm, ActionForm

from gestor.feeds import ActionItemFeed
from activitystream.feeds import ActivityStreamFeed

feeds = {
    'ActionItems': ActionItemFeed,
    'stream': ActivityStreamFeed,
}


urlpatterns = patterns('',
    (r'^$', 'gestor.views.project_dashboard',),
	(r'^project/(?P<object_id>\d+)/$', 'gestor.views.project_detail', ),
	(r'^project/(?P<object_id>\d+)/close/$', 'gestor.views.project_close', ),
	(r'^project/(?P<object_id>\d+)/re-open/$', 'gestor.views.project_reopen', ),
	(r'^project/(?P<object_id>\d+)/fast_edit/$', 'gestor.views.project_fastedit', ),
	(r'^project/(?P<object_id>\d+)/edit/$', 'gestor.views.project_edit', ),
	
	# Note: the following is dangerous if you ever change the project's pk to strings
	(r'^project/create/$', 'gestor.views.project_create', ),
	
    (r'^feeds/(?P<url>.*)/$', 'gestor.views.protected_feed', {'feed_dict': feeds}),
    (r'^ical/ActionItems/(?P<username>([A-z]|[0-9]|[_])+)/$', 'gestor.views.action_ical',),
	
	(r'^action/(?P<object_id>\d+)/$', 'gestor.views.action_detail', ),
	(r'^action/in/(?P<object_id>\d+)/$', 'gestor.views.action_create', ),
	(r'^action/(?P<object_id>\d+)/edit/$', 'gestor.views.action_edit',),
	(r'^action/(?P<object_id>\d+)/delete/$', 'gestor.views.action_delete',),
	(r'^action/(?P<object_id>\d+)/finish/$', 'gestor.views.action_finish', ),

	
	(r'^note/(?P<object_id>\d+)/$', 'gestor.views.note_detail', ),
	(r'^note/in/(?P<object_id>\d+)/$', 'gestor.views.note_create', ),
	(r'^note/(?P<object_id>\d+)/edit/$', 'gestor.views.note_edit',),
	(r'^note/(?P<object_id>\d+)/delete/$', 'gestor.views.note_delete',),
	
	(r'^actionnote/(?P<object_id>\d+)/$', 'gestor.views.actionnote_detail', ),
	(r'^actionnote/in/(?P<object_id>\d+)/$', 'gestor.views.actionnote_create', ),
	(r'^actionnote/(?P<object_id>\d+)/edit/$', 'gestor.views.actionnote_edit',),
	(r'^actionnote/(?P<object_id>\d+)/delete/$', 'gestor.views.actionnote_delete',),
	(r'^search/$', 'gestor.views.search_everything',),

    (r'^stream/(?P<all>all/?)?$', 'activitystream.views.activity_stream',),
    (r'^stream/(?P<stream_id>\d+)/', 'activitystream.views.activity_stream_detail'),

)
