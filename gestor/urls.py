from django.conf.urls.defaults import *
from gestor.models import Project


project_queryset = { 'queryset': Project.objects.all() }

urlpatterns = patterns('',
    (r'^$', 'gestor.views.project_list',),
	(r'^project/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', dict(project_queryset,template_name='project_detail.html')),
)
