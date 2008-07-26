from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import *

from gestor.models import Project, ActionItem, Note
from django.contrib.auth.models import User

from gestor.forms import NoteForm, ActionForm


# Project Views

@login_required
def project_list(request):
	p = request.user.id_worker.all()
	return render_to_response('project_list.html',{'object_list':p})
	
	
@login_required
def project_detail(request,object_id):
	p = Project.objects.get(id=object_id)
	return render_to_response('project_detail.html',{
		'object':p,
		'notes': p.note_set.order_by("-set_date"),
		'actionitems': p.actionitem_set.order_by("due_date")
		})


# Note Views

@login_required
def note_detail(request,object_id):
	p = Note.objects.get(id=object_id)
	return render_to_response('note_detail.html',{'object':p})
	
@login_required
def note_delete(request,object_id):
	r = get_object_or_404(Note,id=object_id)
	r.delete()
	request.user.message_set.create(message='Note %s was deleted' % r.title )
	return HttpResponseRedirect(r.project.get_absolute_url())

@login_required
def note_create(request,object_id):
	
	form_class = NoteForm
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save()
			if request.user.is_authenticated():
				request.user.message_set.create(message="Note %s was updated" % obj.title )
			return HttpResponseRedirect(obj.get_absolute_url())
	else:
		form = form_class(initial={'author':request.user.id,'project':object_id })

	return render_to_response('note_edit.html',{'form':form})

	
@login_required
def note_edit(request,object_id):
	obj = get_object_or_404(Note,id=object_id)
	form_class = NoteForm
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES, instance=obj)
		if form.is_valid():
			
			obj = form.save()
			if request.user.is_authenticated():
				request.user.message_set.create(message="Note %s was updated" % obj.title )
			return HttpResponseRedirect(obj.get_absolute_url())
	else:
		form = form_class(instance=obj)

	return render_to_response('note_edit.html',{'form':form})
		
	


# ActionItem Views

@login_required
def action_detail(request,object_id):
	p = ActionItem.objects.get(id=object_id)
	return render_to_response('action_detail.html',{'object':p})

@login_required
def action_delete(request,object_id):
	r = get_object_or_404(ActionItem,id=object_id)
	r.delete()
	request.user.message_set.create(message='ActionItem %s was deleted' % r.title )
	return HttpResponseRedirect(r.project.get_absolute_url())
	
@login_required
def action_create(request,object_id):
	
	form_class = ActionForm
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save()
			if request.user.is_authenticated():
				request.user.message_set.create(message="ActionItem %s was updated" % obj.title )
			return HttpResponseRedirect(obj.get_absolute_url())
	else:
		form = form_class(initial={'author':request.user.id,'project':object_id })

	return render_to_response('action_edit.html',{'form':form})

	
@login_required
def action_edit(request,object_id):
	obj = get_object_or_404(ActionItem,id=object_id)
	form_class = ActionForm
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES, instance=obj)
		if form.is_valid():
			
			obj = form.save()
			if request.user.is_authenticated():
				request.user.message_set.create(message="Action %s was updated" % obj.title )
			return HttpResponseRedirect(obj.get_absolute_url())
	else:
		form = form_class(instance=obj)

	return render_to_response('action_edit.html',{'form':form})

def action_finish(request, object_id):
	obj = get_object_or_404(ActionItem,id=object_id)
	obj.done = True
	obj.save()
	return action_detail(request,object_id)