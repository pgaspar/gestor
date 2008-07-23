from django.shortcuts import render_to_response, get_object_or_404
from gestor.models import Project
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def project_list(request):
	p = [ e 
		for e in Project.objects.select_related()
		if request.user in e.workers.all() ]
	return render_to_response('project_list.html',{'object_list':p})
	
	

@login_required
def project_detail(request,object_id):
	p = Project.objects.get(id=object_id)
	return render_to_response('project_detail.html',{'object':p})