from django.template import Library

register = Library()

@register.filter
def ismanager(value, obj):
	return value == obj.manager

@register.filter
def manages_user(request_user, u):
	return request_user in [ proj.manager for proj in u.projects_working.filter(active=True) ]