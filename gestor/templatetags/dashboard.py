from django.template import Library

register = Library()

list_size = 3

@register.filter
def team_list(value):
	
	users = [value.manager]
	for user in value.team.all()[:list_size]:
		if user != value.manager: users.append(user)
	
	return users[:list_size]
	
@register.filter
def more_members(value):
	
	team = value.team.all()
	if value.manager in team:
		return len( team ) > list_size
	else:
		return len( team ) + 1 > list_size