from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required

def render(request,template,context={}):
	return render_to_response(template,context,context_instance=RequestContext(request))


@login_required
def profile(request,username):
	u = get_object_or_404(User, username = username)
	current_projects = u.projects_working.filter(active=True)
	past_projects = u.projects_working.filter(active=False)
	todo_list = User.objects.get(username=username).actionitem_todo.filter(done=False).order_by("due_date")
	return render(request,'user_profile.html',{'u':u,'current_projects':current_projects,'past_projects':past_projects,'todo_list':todo_list})
