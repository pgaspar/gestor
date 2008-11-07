from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	(r'^logout/$', 'django.contrib.auth.views.logout_then_login',),
	(r'^profile/$', 'django.views.generic.simple.redirect_to', { 'url': "/" }), 
	(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'password_change.html'}), 
	(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_change_done.html'}), 
	
	(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'password_reset.html'}),
	(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password_reset_done.html'}),
	(r'^password_reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password_reset_confirm.html'}),
	(r'^password_reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password_change_done.html'}),
	
)
