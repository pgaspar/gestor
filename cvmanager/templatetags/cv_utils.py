from django.template import Library
from gestor.utils import work_together

register = Library()

@register.filter
def can_view_this_cv(user, target):
	return user == target or (work_together(user, target) and user.has_perm('cvmanager.can_view_team_cv'))