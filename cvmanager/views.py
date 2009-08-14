from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.template.context import RequestContext
from cvmanager.models import CurriculumVitae

from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import *
from django.forms import *

from cvmanager.forms import CvForm
from django.core.exceptions import PermissionDenied

from django.views.generic.create_update import create_object, update_object

import datetime

def render(request,template,context={}):
	return render_to_response(template,context,context_instance=RequestContext(request))

# Curriculum Views

@login_required
def curriculum(request,username):
	if (request.user.has_perm('cvmanager.can_view_cv') and request.user.has_perm('cvmanager.can_view_cv_details')) or request.user.username == username:
		u = get_object_or_404(User, username = username)
		c = get_object_or_404(CurriculumVitae, owner = u)
		
		try: profile = u.get_profile()
		except UserProfile.DoesNotExist: profile = None
		
		return render(request,'curriculum.html',{'u':u, 'cv':c, 'profile':profile})
	else:
		raise PermissionDenied()

def public_curriculum(request, username):
	# This page will be visible to the outside world (logged out users)
	
	u = get_object_or_404(User, username = username)
	c = get_object_or_404(CurriculumVitae, owner = u)
	
	try: profile = u.get_profile()
	except UserProfile.DoesNotExist: profile = None
	
	return render(request,'public_curriculum.html',{'u':u, 'cv':c, 'profile':profile})
	
@login_required
def edit_my_curriculum(request):
	u = request.user
	
	if u.curriculumvitae_set.count(): cv = CurriculumVitae.objects.get(owner=u)
	else: cv = None
	
	if request.method == 'POST':
		POST = request.POST.copy()
		POST['owner'] = u.id
		
		form = CvForm(POST, request.FILES, instance=cv)
		
		if form.is_valid():
			cv = form.save()

			request.user.message_set.create(message="Your Curriculum was updated")
			return HttpResponseRedirect(cv.get_absolute_url())
	else:
		if cv: form = CvForm(instance=cv)
		else: form = CvForm(initial={'user':request.user})
	
	return render(request, 'curriculum_edit.html', {'form':form})
