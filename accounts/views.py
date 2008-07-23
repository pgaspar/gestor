from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User


def profile(request,username):
	u = get_object_or_404(User, username = username)
	return render_to_response('user_profile.html',{'user':u})
