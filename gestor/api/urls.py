from django.conf.urls.defaults import *

# Final URL extension
# Examples: /show /show.m /show.xml /show.json
ext = r'(\.(?P<extension>\w{1,4}))?$'

urlpatterns = patterns('',
    
    # Action Items
    (r'^action_items'                        + ext,  'gestor.api.views.action_items',),
    (r'^action_items/todo'                       + ext,  'gestor.api.views.action_items_todo',),
    (r'^action_items/(?P<item_id>\d+)'      + ext,  'gestor.api.views.action_item',),
    
    # Projects
    (r'^projects'                        + ext,  'gestor.api.views.projects',),
    (r'^projects/(?P<project_id>\d+)'   + ext,  'gestor.api.views.projects_show',),
)
