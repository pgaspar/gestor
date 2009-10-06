from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from accounts.models import UserProfile
from accounts.forms import UserProfileForm, UserForm

from django.contrib.auth.decorators import login_required

from gestor.utils import dist, work_together, mergeLists
from common.utils import render
from common.views import PermissionDenied

# Redirects

@login_required
def redirect_to_profile(request):
	return HttpResponseRedirect('/users/' + request.user.username)
	
# Accounts Views
	
@login_required
def profile(request,username):
	u = get_object_or_404(User, username = username)
	
	if not (request.user == u or request.user.has_perm('accounts.view_profiles') or work_together(u, request.user)):
		return PermissionDenied(request)
	
	current_projects = mergeLists(u.projects_working.filter(active=True), u.projects_managed.filter(active=True))
	past_projects = mergeLists(u.projects_working.filter(active=False), u.projects_managed.filter(active=False))
	todo_list = [ [item, dist(item.due_date)] for item in u.actionitem_todo.filter(done=False) ]
	
	try: profile = u.get_profile()
	except UserProfile.DoesNotExist: profile = None
	
	return render(request,'user_profile.html',{'u':u,'current_projects':current_projects,'past_projects':past_projects,'todo_list':todo_list, 'profile':profile})

@login_required
def edit_my_profile(request):
	u = request.user
	
	try: profile = u.get_profile()
	except UserProfile.DoesNotExist: profile = None
	
	if request.method == 'POST':
		POST = request.POST.copy()
		POST['user'] = u.id
		
		profile_form = UserProfileForm(POST, request.FILES, instance=profile)
		user_form = UserForm(request.POST, request.FILES, instance=u)
		
		if user_form.is_valid() and profile_form.is_valid():
			u = user_form.save()
			profile = profile_form.save()
			profile.user = u
			
			request.user.message_set.create(message="Your Profile was updated")
			
			return HttpResponseRedirect(profile.get_absolute_url())
	else:
		user_form = UserForm(instance=u)
		
		if profile: profile_form = UserProfileForm(instance=profile)
		else: profile_form = UserProfileForm(initial={'user':request.user})
		
	return render(request, 'edit_profile.html', {'profile_form':profile_form, 'user_form':user_form})