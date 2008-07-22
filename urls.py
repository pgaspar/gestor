from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^gestor/', include('jksite.gestor.urls')),

    (r'^$', 'django.views.generic.simple.redirect_to', { 'url': "/gestor/" }),
)
