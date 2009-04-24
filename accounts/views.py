from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template.context import RequestContext

from accounts.models import UserProfile

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from gestor.utils import dist, work_together


def render(request,template,context={}):
	return render_to_response(template,context,context_instance=RequestContext(request))


@login_required
def profile(request,username):
	u = get_object_or_404(User, username = username)
	
	if not (request.user == u or request.user.has_perm('accounts.view_profiles') or work_together(u, request.user)):
		raise PermissionDenied()
	
	current_projects = list(set(u.projects_working.filter(active=True)) | set(u.projects_managed.filter(active=True)))
	past_projects = list(set(u.projects_working.filter(active=False)) | set(u.projects_managed.filter(active=False)))
	todo_list = [ [item, dist(item.due_date)] for item in User.objects.get(username=username).actionitem_todo.filter(done=False) ]
	
	try: profile = u.get_profile()
	except UserProfile.DoesNotExist: profile = None
	
	return render(request,'user_profile.html',{'u':u,'current_projects':current_projects,'past_projects':past_projects,'todo_list':todo_list, 'profile':profile})
