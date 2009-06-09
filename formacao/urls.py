from django.conf.urls.defaults import *
from formacao.models import Event

from datetime import datetime

urlpatterns = patterns('',
	(r'^formacao/$', 'django.views.generic.list_detail.object_list', {'template_name': 'formacao.html', 'queryset': Event.objects.filter(date__gte=datetime.now()).order_by("date")}),
	(r'^formacao/$', 'django.views.generic.list_detail.object_list', {'template_name': 'formacao.html', 'queryset': Event.objects.filter(date__lt=datetime.now()).order_by("date"), 'extra_context':{'old':'true'}}),
	
	(r'^formacao/(?P<object_id>\d+)/$', 'formacao.views.view_content', {'template_name': 'event_detail.html'}),
	(r'^formacao/(?P<object_id>\d+)/private/$', 'formacao.views.view_private_content'),
)