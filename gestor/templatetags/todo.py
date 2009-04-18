from django.template import Library
from django.contrib.auth.models import User

from gestor.utils import color_status, dist, truncate

register = Library()

@register.filter
def todo(value):
	max_word = 4
	return "<ul>" + "\n".join([ ("<li class='%s'><a href='%s' title='%s days left in %s with %s priority'>%s</a></li>" % ( color_status(obj),obj.get_absolute_url(),dist(obj.due_date),obj.project.name,obj.get_priority_display(),truncate(obj.title, max_word)) ) for obj in User.objects.get(username=value).actionitem_todo.filter(done=False) ]) + "</ul>"