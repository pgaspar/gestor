from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import *

from gestor.models import Project, ActionItem, Note
from django.contrib.auth.models import User

from django.forms import *
from gestor.forms import NoteForm, ActionForm

def render(request,template,context={}):
	return render_to_response(template,context,context_instance=RequestContext(request))



# General Views

def create_view(request,object_id,form_class,template_name):
	model = form_class.Meta.model
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save()
			if request.user.is_authenticated():
				request.user.message_set.create(message="The %s was updated" % model._meta.verbose_name )
			return HttpResponseRedirect(obj.get_absolute_url())
	else:
		form = form_class(initial={'author':request.user.id,'project':object_id })

	return render(request,template_name,{'form':form})


def edit_view(request,object_id,form_class,template_name):
	model = form_class.Meta.model
	obj = get_object_or_404(model,id=object_id)
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES, instance=obj)
		if form.is_valid():
			
			obj = form.save()
			if request.user.is_authenticated():
				request.user.message_set.create(message="The %s was updated" % model._meta.verbose_name )
			return HttpResponseRedirect(obj.get_absolute_url())
	else:
		form = form_class(instance=obj)
	if model == ActionItem:
		form['targets'] = ModelMultipleChoiceField(queryset=obj.project.team.all())
	return render(request,template_name,{'form':form})

def delete_view(request,object_id,model):
	obj = get_object_or_404(model,id=object_id)
	obj.delete()
	request.user.message_set.create(message='The %s was deleted' % model._meta.verbose_name )
	return HttpResponseRedirect(obj.project.get_absolute_url())



# Project Views

@login_required
def project_list(request):
	p = request.user.projects_working.all()
	return render(request,'project_list.html',{'object_list':p})
	
	
@login_required
def project_detail(request,object_id):
	p = Project.objects.get(id=object_id)
	return render(request,'project_detail.html',{
		'object':p,
		'notes': p.note_set.order_by("-set_date"),
		'actionitems': p.actionitem_set.order_by("due_date")
		})


# Note Views

@login_required
def note_detail(request,object_id):
	p = Note.objects.get(id=object_id)
	return render(request,'note_detail.html',{'object':p})
	
@login_required
def note_delete(request,object_id):
	return delete_view(request,object_id,Note)

@login_required
def note_create(request,object_id):
	return create_view(request,object_id,NoteForm,"note_edit.html")

	
@login_required
def note_edit(request,object_id):
	return edit_view(request,object_id,NoteForm,"note_edit.html")


# ActionItem Views

@login_required
def action_detail(request,object_id):
	p = ActionItem.objects.get(id=object_id)
	return render(request,'action_detail.html',{'object':p})

@login_required
def action_delete(request,object_id):
	return delete_view(request,object_id,ActionItem)
	
@login_required
def action_create(request,object_id):
	return create_view(request,object_id,ActionForm,"action_edit.html")

	
@login_required
def action_edit(request,object_id):
	return edit_view(request,object_id,ActionForm,"action_edit.html")
	

def action_finish(request, object_id):
	obj = get_object_or_404(ActionItem,id=object_id)
	obj.done = True
	obj.save()
	return action_detail(request,object_id)