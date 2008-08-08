from django.template import Library
from datetime import date
from django.contrib.auth.models import User

from gestor.utils import color_status

register = Library()



def dist(d):
	dif =  d - date.today()
	return str(dif.days)

@register.filter
def todo(value):
	return "<ul>" + "\n".join([ ("<li class='%s'><a href='%s' title='%s days left in %s'>%s</a></li>" % ( color_status(obj),obj.get_absolute_url(),dist(obj.due_date),obj.project.name,obj.title) ) for obj in User.objects.get(username=value).actionitem_todo.filter(done=False).order_by("due_date") ]) + "</ul>"