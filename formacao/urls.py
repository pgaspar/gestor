from django.conf.urls.defaults import *
from formacao.models import Event

from datetime import date

urlpatterns = patterns('',
	(r'^$', 'django.views.generic.list_detail.object_list', {'template_name': 'formacao.html', 'queryset': Event.objects.filter(date__gte=date.today(), is_published=True).order_by("date")}),
	(r'^old/$', 'django.views.generic.list_detail.object_list', {'template_name': 'formacao.html', 'queryset': Event.objects.filter(date__lt=date.today(), is_published=True).order_by("-date"), 'extra_context':{'old':'true'}}),
	
	
	
	(r'^(?P<object_id>\d+)/$', 'formacao.views.view_content'),
	(r'^(?P<slug>[-\w]+)/$', 'formacao.views.view_content_with_slug'),
	(r'^(?P<object_id>\d+)/private/$', 'formacao.views.view_private_content'),
	
	(r'^(?P<object_id>\d+)/inscrever/$', 'formacao.views.surveys', {'register':True}),
	(r'^(?P<object_id>\d+)/confirm/$', 'formacao.views.surv_response'),
	
	(r'^(?P<object_id>\d+)/inquerito/$', 'formacao.views.surveys', {'register':False}),
	(r'^thanks/$', 'django.views.generic.simple.direct_to_template', {'template': 'survey_thanks.html'}),
)