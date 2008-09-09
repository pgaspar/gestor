from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import *

from gestor.models import Project, ActionItem, Note, File
from django.contrib.auth.models import User

from django.forms import *
from gestor.forms import NoteForm, ActionForm, FileForm

from django.core.mail import send_mail

from settings import *
from common.utils import render


# General Views

def create_view(request,object_id,form_class,template_name):
	model = form_class.Meta.model
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save()
			if request.user.is_authenticated():
				request.user.message_set.create(message="The %s was created" % model._meta.verbose_name )
			if form.cleaned_data['notification']:
				send_mail( "[%s] New %s: %s" % (obj.project.name,model._meta.verbose_name,obj.title),
					'%s created a new %s in project %s entitled "%s" \n\n Link: %s' % (request.user.get_full_name(), model._meta.verbose_name, obj.project.name,obj.title,BASE_DOMAIN + obj.get_absolute_url()), 
					EMAIL_FROM,
					[ user.email for user in obj.project.team.all() ])
			return HttpResponseRedirect(obj.get_absolute_url())
	else:
		form = form_class(initial={'author':request.user.id,'project':object_id })

	if model == ActionItem:
		form.fields['targets'] = ModelMultipleChoiceField(queryset=Project.objects.get(id=object_id).team.all())
	return render(request,template_name,{'form':form})


def edit_view(request,object_id,form_class,template_name):
	model = form_class.Meta.model	
	obj = get_object_or_404(model,id=object_id)
	obj.project.check_user(request.user)
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES, instance=obj)
		if form.is_valid():
			
			obj = form.save()
			if request.user.is_authenticated():
				request.user.message_set.create(message="The %s was updated" % model._meta.verbose_name )
			if form.cleaned_data['notification']:
				send_mail( "[%s] %s edited: %s" % (obj.project.name,model._meta.verbose_name,obj.title),
					'%s edited a %s in project %s entitled "%s" \n\n Link: %s' % (request.user.get_full_name(), model._meta.verbose_name, obj.project.name,obj.title,BASE_DOMAIN + obj.get_absolute_url()), 
					EMAIL_FROM,
					[ user.email for user in obj.project.team.all() ])
			return HttpResponseRedirect(obj.get_absolute_url())
	else:
		form = form_class(instance=obj)
	if model == ActionItem:
		form.fields['targets'] = ModelMultipleChoiceField(queryset=obj.project.team.all())
	return render(request,template_name,{'form':form})

def delete_view(request,object_id,model):
	obj = get_object_or_404(model,id=object_id)
	obj.project.check_user(request.user)
	obj.delete()
	request.user.message_set.create(message='The %s was deleted' % model._meta.verbose_name )
	return HttpResponseRedirect(obj.project.get_absolute_url())



# Project Views

@login_required
def project_list(request):
	if request.user.is_staff:
		p = Project.objects.all()
	else:
		p = request.user.projects_working.all()
	return render(request,'project_list.html',{'object_list':p})
	
	
@login_required
def project_detail(request,object_id):
	p = Project.objects.get(id=object_id)
	p.check_user(request.user)
	
	return render(request,'project_detail.html',{
		'object':p,
		'notes': p.note_set.order_by("-set_date"),
		'files': p.file_set.order_by("-set_date"),
		'actionitems': p.actionitem_set.order_by("done","due_date")
		})


# Note Views

@login_required
def note_detail(request,object_id):
	p = Note.objects.get(id=object_id)
	p.project.check_user(request.user)
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

# File Views

@login_required
def file_detail(request,object_id):
	p = File.objects.get(id=object_id)
	p.project.check_user(request.user)
	return render(request,'file_detail.html',{'object':p})

@login_required
def file_delete(request,object_id):
	return delete_view(request,object_id,File)

@login_required
def file_create(request,object_id):
	return create_view(request,object_id,FileForm,"file_edit.html")


@login_required
def file_edit(request,object_id):
	return edit_view(request,object_id,FileForm,"file_edit.html")


# ActionItem Views

@login_required
def action_detail(request,object_id):
	p = ActionItem.objects.get(id=object_id)
	p.project.check_user(request.user)
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
	
@login_required
def action_finish(request, object_id):
	obj = get_object_or_404(ActionItem,id=object_id)
	obj.done = True
	obj.save()
	return action_detail(request,object_id)
	
def action_ical(request,username):
	user = get_object_or_404(User,username=username)
	todos = user.actionitem_todo.filter(done=False)
	filename = "JK_Gestor_ActionItems.ics"
	
	import vobject
	import datetime
	
	cal = vobject.iCalendar()
	cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this
	
	for actionitem in todos:
		vtodo = cal.add('vtodo')
		vtodo.add('summary').value = actionitem.title
		vtodo.add('description').value = actionitem.description
		vtodo.add('due;value=date').value = actionitem.due_date.strftime("%Y%m%d")
		vtodo.add('priority').value = "0"
		
	
	icalstream = cal.serialize()
	response = HttpResponse(icalstream, mimetype='text/calendar')
	response['Filename'] = filename  # IE needs this
	response['Content-Disposition'] = 'attachment; filename='+filename
	return response