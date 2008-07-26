from django.template import Library
from datetime import date

register = Library()


@register.filter
def colorstatus(value):
	if value.done:
		return "green"
	if value.due_date > date.today():
		return "yellow"
	return "red"