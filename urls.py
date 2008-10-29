from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings


from mainsite.models import News
from mainsite.feeds import NewsFeed

feeds = {
    'noticias': NewsFeed,
}

info_dict = {
    'queryset': News.objects.all(),
    'date_field': 'date',
}



admin.autodiscover()

urlpatterns = patterns('',
	(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^gestor/', include('jksite.gestor.urls')),
    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/$', 'accounts.views.profile'),
    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/curriculum/$', 'cvmanager.views.curriculum'),
    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/curriculum/create/$', 'cvmanager.views.curriculum_create'),
    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/curriculum/edit/$', 'cvmanager.views.curriculum_edit'),
    (r'^accounts/', include('jksite.accounts.urls')),



    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
	
	(r'^noticias/$', 'django.views.generic.list_detail.object_list', {'template_name': 'news_list.html', 'queryset': News.objects.all()}),
	(r'^noticias/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', {'template_name': 'news_detail.html', 'queryset': News.objects.all()}),

    (r'^$', 'django.views.generic.simple.redirect_to', { 'url': "/apresentacao/" }),


)
