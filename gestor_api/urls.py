from django.conf.urls.defaults import *

ext = r'(\.(?P<extension>\w{1,4}))?$'

urlpatterns = patterns('',
    
    # Action Items
    (r'^action_items/all'                        +ext,  'gestor_api.views.action_items_all',),
    (r'^action_items/todo'                       +ext,  'gestor_api.views.action_items_todo',),
    (r'^action_items/create'                     +ext,  'gestor_api.views.action_items_create',),
    (r'^action_items/(?P<item_id>\d+)/show'      +ext,  'gestor_api.views.action_items_show',),
    (r'^action_items/(?P<item_id>\d+)/update'    +ext,  'gestor_api.views.action_items_update',),
    (r'^action_items/(?P<item_id>\d+)/delete'    +ext,  'gestor_api.views.action_items_delete',),
    
    # Projects
    (r'^projects/all'                        +ext,  'gestor_api.views.projects_all',),
    (r'^projects/(?P<project_id>\d+)/show'   +ext,  'gestor_api.views.projects_show',),
)
