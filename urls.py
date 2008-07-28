from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from gestor.feeds import ActionItemFeed

admin.autodiscover()

feeds = {
    'ActionItems': ActionItemFeed,
}

urlpatterns = patterns('',
	(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^gestor/', include('jksite.gestor.urls')),

    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/$', 'accounts.views.profile'),
    (r'^accounts/', include('jksite.accounts.urls')),

    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

    (r'^$', 'django.views.generic.simple.redirect_to', { 'url': "/gestor/" }),
)
