from django.template import Library
from gestor.utils import mergeLists

register = Library()

@register.filter
def workspace(user):
	return mergeLists(user.projects_working.filter(active=True), user.projects_managed.filter(active=True))