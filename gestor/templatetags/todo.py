from django.template import Library
from datetime import date
from django.contrib.auth.models import User

register = Library()


def dist(d):
	dif =  d - date.today()
	return str(dif.days)

@register.filter
def todo(value):
	return "<ul>" + "\n".join([ ("<li><a href='%s' title='%s days left'>%s</a></li>" % ( obj.get_absolute_url(),dist(obj.due_date),obj.title) ) for obj in User.objects.get(username=value).id_target.filter(done=False).order_by("due_date") ]) + "</ul>"