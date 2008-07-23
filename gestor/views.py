from django.shortcuts import render_to_response, get_object_or_404
from gestor.models import Project
from django.contrib.auth.models import User

def project_list(request):
	p = [ e for e in list(Project.objects.all()) if request.user in e.workers ]
	return render_to_response('project_detail.html',{'object_list':p})