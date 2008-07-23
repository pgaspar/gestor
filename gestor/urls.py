from django.conf.urls.defaults import *
from gestor.models import Project


urlpatterns = patterns('gestor.views',
    (r'^$', 'project_list',),
	(r'^project/(?P<object_id>\d+)/$', 'project_detail', ),
)
