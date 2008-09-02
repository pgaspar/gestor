from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
	(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^gestor/', include('jksite.gestor.urls')),

    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/$', 'accounts.views.profile'),
    (r'^users/(?P<username>([A-z]|[0-9]|[_])+)/curriculum/$', 'curriculos.views.curriculum'),
    (r'^accounts/', include('jksite.accounts.urls')),

    (r'^$', 'django.views.generic.simple.redirect_to', { 'url': "/gestor/" }),
)
