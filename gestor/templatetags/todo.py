from django.template import Library
from django.contrib.auth.models import User

from gestor.utils import color_status, dist, truncate

register = Library()

@register.filter
def todo(value):
	max_letters = 25
	f = lambda x: x and (x + ' days left') or 'No due date'
	
	return "<ul>" + "\n".join([ ("<li class='%s'><a href='%s' title='%s in %s with %s priority'>%s</a></li>" % ( color_status(obj),obj.get_absolute_url(),f(dist(obj.due_date)),obj.project.name,obj.get_priority_display(),truncate(obj.title, max_letters)) ) for obj in User.objects.get(username=value).actionitem_todo.filter(done=False) ]) + "</ul>"