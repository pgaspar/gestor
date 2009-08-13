from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template.context import RequestContext
from django.http import HttpResponseRedirect

from accounts.models import UserProfile
from accounts.forms import UserProfileForm

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from gestor.utils import dist, work_together, mergeLists


def render(request,template,context={}):
	return render_to_response(template,context,context_instance=RequestContext(request))


@login_required
def profile(request,username):
	u = get_object_or_404(User, username = username)
	
	if not (request.user == u or request.user.has_perm('accounts.view_profiles') or work_together(u, request.user)):
		raise PermissionDenied()
	
	current_projects = mergeLists(u.projects_working.filter(active=True), u.projects_managed.filter(active=True))
	past_projects = mergeLists(u.projects_working.filter(active=False), u.projects_managed.filter(active=False))
	todo_list = [ [item, dist(item.due_date)] for item in u.actionitem_todo.filter(done=False) ]
	
	try: profile = u.get_profile()
	except UserProfile.DoesNotExist: profile = None
	
	return render(request,'user_profile.html',{'u':u,'current_projects':current_projects,'past_projects':past_projects,'todo_list':todo_list, 'profile':profile})

@login_required
def edit_profile(request):
	u = request.user
	
	try: profile = u.get_profile()
	except UserProfile.DoesNotExist: profile = None
	
	if request.method == 'POST':
		request.POST['user'] = request.user.id
		profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
		
		if profile_form.is_valid():
			profile = profile_form.save()

			request.user.message_set.create(message="Your Profile was updated")

			return HttpResponseRedirect(profile.get_absolute_url())
	else:
		if profile: profile_form = UserProfileForm(instance=profile)
		else: profile_form = UserProfileForm(initial={'user':request.user})
	
	return render(request, 'edit_profile.html', {'profile_form':profile_form})