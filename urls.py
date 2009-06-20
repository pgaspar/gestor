from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings


from mainsite.models import News
from mainsite.feeds import NewsFeed

feeds = {
    'noticias': NewsFeed,
}

info_dict = {
    'queryset': News.objects.filter(is_published=True),
    'date_field': 'date',
    'allow_empty': 1,
}


admin.autodiscover()

urlpatterns = patterns('',
	(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	(r'^dynamic-media/jsi18n/$', 'django.views.i18n.javascript_catalog'), 

	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^gestor/', include('gestor.urls')),
    (r'^users/find/$', 'cvmanager.views.curriculum_find'),
    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/$', 'accounts.views.profile'),
    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/curriculum/$', 'cvmanager.views.curriculum'),
    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/curriculum/create/$', 'cvmanager.views.curriculum_create'),
    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/curriculum/edit/$', 'cvmanager.views.curriculum_edit'),
    (r'^accounts/', include('accounts.urls')),



    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
	
    # News Archives
    (r'^noticias/arquivo/$', 'mainsite.views.archive'),
	(r'^noticias/arquivo/(?P<year>\d{4})/$', 'django.views.generic.date_based.archive_year', dict( info_dict, template_name='news_archive_year.html' )),
    (r'^noticias/arquivo/(?P<year>\d{4})/(?P<month>\w{1,2})/$', 'django.views.generic.date_based.archive_month', dict( info_dict, 
                                                                                                                       month_format='%m',
                                                                                                                       template_name='news_archive_month.html',
                                                                                                                       extra_context={'truncate':'true'})),
    (r'^noticias/arquivo/(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', 'django.views.generic.date_based.archive_day', dict( info_dict,
                                                                                                                                      month_format='%m',
                                                                                                                                      template_name='news_archive_day.html',
                                                                                                                                      extra_context={'truncate':'true'})),
    
	(r'^noticias/(?P<object_id>\d+)/$', 'mainsite.views.news_detail', {'template_name': 'news_detail.html'}),
    
    
    (r'^noticias/create/$', 'mainsite.views.create_news'),

    
    
    # New site (hard-coded, no more flat pages)
    (r'^$', 'mainsite.views.news_index', dict( info_dict, template_name='index.html', num_latest=3 )),
    (r'^carreiras/$', 'django.views.generic.simple.direct_to_template', {'template': 'carreiras.html'}),
    (r'^contactos/$', 'django.views.generic.simple.direct_to_template', {'template': 'contactos.html'}),
    (r'^parceiros/$', 'django.views.generic.simple.direct_to_template', {'template': 'parceiros.html'}),
    (r'^servicos/$', 'django.views.generic.simple.direct_to_template', {'template': 'servicos.html'}),
    (r'^sobre/$', 'django.views.generic.simple.direct_to_template', {'template': 'sobre.html'}),
    
    # Survey
    (r'^formacao/inquerito/$', 'django.views.generic.simple.direct_to_template', {'template': 'inquerito.html'}),
    (r'^formacao/$', 'django.views.generic.simple.redirect_to', { 'url': "/" }),
    
    # Public curriculums
    (r'^(?P<username>([A-z]|[0-9]|[_])+)/$', 'cvmanager.views.public_curriculum'),
    

)
