from django.template import Library
from gestor.utils import truncate

register = Library()

@register.filter
def team_list(value):
	
	users = [value.manager]
	for user in value.team.all():
		if user != value.manager:
			users.append(user)
	return users
	
@register.filter
def trunc(txt, lim):
	return truncate(txt, lim)
	
@register.filter
def bigger_than(val1, val2):
	return int(val1) > int(val2)