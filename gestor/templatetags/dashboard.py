from django.template import Library

register = Library()

@register.filter
def team_list(value):
	
	users = [value.manager]
	for user in value.team.all()[:3]:
		if user != value.manager: users.append(user)
	
	return users[:3]
	
@register.filter
def more_members(value):
	listed_members = 3
	
	if value.manager in value.team.all():
		return len( value.team.all() ) > listed_members
	else:
		return len( value.team.all() ) + 1 > listed_members