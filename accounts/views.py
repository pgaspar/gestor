from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template.context import RequestContext

def render(request,template,context={}):
	return render_to_response(template,context,context_instance=RequestContext(request))


def profile(request,username):
	u = get_object_or_404(User, username = username)
	current_projects = u.projects_working.filter(status=True)
	past_projects = u.projects_working.filter(status=False)
	return render(request,'user_profile.html',{'u':u,'current_projects':current_projects,'past_projects':past_projects})
