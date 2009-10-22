from django.conf.urls.defaults import *
from models import Entity

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {'template_name': 'ecosystem.html', 'queryset': Entity.objects.all()}),

)