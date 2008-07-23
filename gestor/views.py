from django.shortcuts import render_to_response, get_object_or_404
from gestor.models import Project
from django.contrib.auth.models import User

def project_list(request):
	#p = Project.objects.filter(workers=request.user)
	return render_to_response('project_detail.html',{'object_list':p})