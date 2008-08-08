from django.template import Library
from gestor.utils import color_status

register = Library()


@register.filter
def colorstatus(value):
	return color_status(value)