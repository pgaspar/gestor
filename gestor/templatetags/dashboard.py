from django.template import Library

register = Library()

@register.filter
def team_list(value):
	
	users = [value.manager]
	for user in value.team.all()[:3]:
		if user != value.manager: users.append(user)
	
	return users[:3]

@register.filter
def user_class(value):
	pass
	
@register.filter
def more_members(value):
	listed_members = 3
	
	return len( value ) > listed_members