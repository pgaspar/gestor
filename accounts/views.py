from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
# from gestor.models import Project


def profile(request,username):
	u = get_object_or_404(User, username = username)
	current_projects = u.id_worker.filter(status=True)
	past_projects = u.id_worker.filter(status=False)
	return render_to_response('user_profile.html',{'user':u,'current_projects':current_projects,'past_projects':past_projects})
