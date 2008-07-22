from django.conf.urls.defaults import *
from gestor.models import Project


project_queryset = { 'queryset': Project.objects.all() }

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', dict(project_queryset,template_name='project_list.html') ),
	(r'^project/(?P<object_id>\d+)/$', 'object_detail', dict(project_queryset,template_name='project_detail.html')),
)
