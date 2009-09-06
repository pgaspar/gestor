from django.conf.urls.defaults import *

ext = r'(\.(?P<extension>\w{1,4}))?$'

urlpatterns = patterns('',
    
    # Action Items
    (r'^action_items/todo'     +ext,  'gestor_api.views.action_items_todo',),
    (r'^action_items/create'   +ext,  'gestor_api.views.action_items_create',),
    (r'^action_items/update'   +ext,  'gestor_api.views.action_items_update',),
    
    # Projects
)
