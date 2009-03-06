from django.template import Library

register = Library()

@register.filter
def ismanager(value, obj):
	return value == obj.manager