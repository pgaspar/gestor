from django.template import Library

register = Library()

@register.filter
def workspace(value):
	return value.filter(active=True)