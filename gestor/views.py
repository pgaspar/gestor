from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import *

from gestor.models import Project, ActionItem, Note
from django.contrib.auth.models import User


@login_required
def project_list(request):
	p = request.user.id_worker.all()
	return render_to_response('project_list.html',{'object_list':p})
	
	

@login_required
def project_detail(request,object_id):
	p = Project.objects.get(id=object_id)
	return render_to_response('project_detail.html',{'object':p})


@login_required
def note_detail(request,object_id):
	p = Note.objects.get(id=object_id)
	return render_to_response('note_detail.html',{'object':p})


@login_required
def note_edit(request,object_id):
	return update_object(request, object_id = object_id, model=Note, template_name='note_edit.html')

@login_required
def note_delete(request,object_id):
	r = get_object_or_404(Note,id=object_id)
	r.delete()
	request.user.message_set.create(message='Note %s was deleted' % r.title )
	return HttpResponseRedirect(r.project.get_absolute_url())