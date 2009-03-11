from django.template import Library

register = Library()

@register.filter
def team_list(value):
	
	users = [value.manager]
	for user in value.team.all():
		if user != value.manager:
			users.append(user)
	return users