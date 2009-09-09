from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import *

from django.contrib.syndication.views import feed

from gestor.models import Project, ActionItem, Note, ActionNote, File
from cvmanager.models import CurriculumVitae
from accounts.models import UserProfile
from django.contrib.auth.models import User

from django.core.exceptions import PermissionDenied

from django.forms import *
from gestor.forms import NoteForm, ActionForm, FileForm, ActionNoteForm, ProjectForm, SearchForm

from django.db.models import Q
from django.core.mail import send_mail

from settings import *
from common.utils import render
from gestor.utils import dist, mergeLists

from datetime import date


# General Views

def create_view(request,object_id,form_class,template_name):
	model = form_class.Meta.model	# Never a Project
	
	if model is ActionNote:
		obj = get_object_or_404(ActionItem,id=object_id).project
	else:
		obj = get_object_or_404(Project,id=object_id)
	
	if not (request.user.has_perm('gestor.add_' + model._meta.module_name) or obj.has_user(request.user)):
		raise PermissionDenied()
	
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save()
			if request.user.is_authenticated():
				request.user.message_set.create(message="The %s was created" % model._meta.verbose_name )
			if form.cleaned_data['notification']:
				if model is ActionNote:
					send_mail( "[%s] New %s by %s" % (obj.actionitem.title,model._meta.verbose_name,request.user.get_full_name()),
						'%s created a new %s in action item %s whith the following description:\n\n "%s" \n\nLink: %s' % (request.user.get_full_name(), model._meta.verbose_name, obj.actionitem.title,obj.description,BASE_DOMAIN + obj.actionitem.get_absolute_url()), 
						DEFAULT_FROM_EMAIL,
						[ user.email for user in obj.actionitem.targets.all() if not user == request.user ])
				else:
					send_mail( "[%s] New %s: %s" % (obj.project.name,model._meta.verbose_name,obj.title),
						'%s created a new %s in project %s entitled "%s" \n\n Link: %s' % (request.user.get_full_name(), model._meta.verbose_name, obj.project.name,obj.title,BASE_DOMAIN + obj.get_absolute_url()), 
						DEFAULT_FROM_EMAIL,
						[ user.email for user in obj.project.team.all() if not user == request.user ])
			if model is ActionNote:
				return HttpResponseRedirect(obj.actionitem.get_absolute_url())
			else:
				return HttpResponseRedirect(obj.get_absolute_url())
	else:
		if model is ActionNote:
			form = form_class(initial={'author':request.user.id,'actionitem':object_id })
		else:
			form = form_class(initial={'author':request.user.id,'project':object_id })

	if model == ActionItem:
		form.fields['targets'] = ModelMultipleChoiceField(queryset=Project.objects.get(id=object_id).team.all())
	return render(request,template_name,{'form':form})


def edit_view(request,object_id,form_class,template_name):
	model = form_class.Meta.model	
	obj = get_object_or_404(model,id=object_id)
	
	if model is ActionNote: proj = obj.actionitem.project
	else: proj = obj.project

	if not (request.user.has_perm('gestor.change_' + model._meta.module_name) or proj.has_user(request.user)):
		raise PermissionDenied()

	if request.method == 'POST':
		form = form_class(request.POST, request.FILES, instance=obj)
		if form.is_valid():

			obj = form.save()
			if request.user.is_authenticated():
				request.user.message_set.create(message="The %s was updated" % model._meta.verbose_name )
			if form.cleaned_data['notification']:

				if model == ActionItem:
					full_desc = "For: %s\n\n%s" % (", ".join([ e.get_full_name() for e in obj.targets.all() ]), obj.description)
				elif model == Note:
					full_desc = "%s" % obj.description
				else:
					full_desc = ""

				if model is ActionNote:
					send_mail( "[%s] %s edited by %s" % (obj.actionitem.title,model._meta.verbose_name,request.user.get_full_name()),
						'%s edited a %s in action item %s whith the following description:\n\n "%s" \n\nLink: %s\n\n %s' % (request.user.get_full_name(), model._meta.verbose_name, obj.actionitem.title,obj.description,BASE_DOMAIN + obj.actionitem.get_absolute_url(),full_desc), 
						DEFAULT_FROM_EMAIL,
						[ user.email for user in obj.actionitem.targets.all() if not user == request.user ])
				else:
					send_mail( "[%s] %s edited: %s" % (obj.project.name,model._meta.verbose_name,obj.title),
						'%s edited a %s in project %s entitled "%s" \n\n Link: %s\n\n %s' % (request.user.get_full_name(), model._meta.verbose_name, obj.project.name,obj.title,BASE_DOMAIN + obj.get_absolute_url(),full_desc), 
						DEFAULT_FROM_EMAIL,
						[ user.email for user in obj.project.team.all() if not user == request.user ])
			if model is ActionNote:
				return HttpResponseRedirect(obj.actionitem.get_absolute_url())
			else:
				return HttpResponseRedirect(obj.get_absolute_url())
	else:
		form = form_class(instance=obj)
	if model == ActionItem:
		form.fields['targets'] = ModelMultipleChoiceField(queryset=obj.project.team.all())
	return render(request,template_name,{'form':form})

def delete_view(request,object_id,model):
	obj = get_object_or_404(model,id=object_id)
	
	if model is ActionNote: proj = obj.actionitem.project
	else: proj = obj.project

	if not (request.user.has_perm('gestor.delete_' + model._meta.module_name) or proj.has_user(request.user)):
		raise PermissionDenied()
	
	obj.delete()
	request.user.message_set.create(message='The %s was deleted' % model._meta.verbose_name )
	if model is ActionNote:
		return HttpResponseRedirect(obj.actionitem.get_absolute_url())
	else:
		return HttpResponseRedirect(obj.project.get_absolute_url())



# Project Views

@login_required
def project_edit(request, object_id):
	p = get_object_or_404(Project,id=object_id)

	p.check_manager(request.user, 'change')

	if request.method == 'POST':
		form = ProjectForm(request.POST, instance = p)

		if form.is_valid():
			p = form.save()

			request.user.message_set.create(message="The Project was updated")

			return HttpResponseRedirect(p.get_absolute_url())
	else:
		form = ProjectForm(instance = p)
	
	return render(request,"project_edit.html",{'form':form})
		

@login_required
def project_create(request):
	if request.user.has_perm('gestor.add_project'):
		p = Project()
		
		if request.method == 'POST':
			form = ProjectForm(request.POST, instance = p)
			
			if form.is_valid():
				p = form.save()
				
				request.user.message_set.create(message="Project Created")
				
				return HttpResponseRedirect(p.get_absolute_url())
		else:
			form = ProjectForm(instance = p)
		return render(request,"project_edit.html",{'form':form})
		
	else:
		raise PermissionDenied()

@login_required
def project_fastedit(request, object_id):
	if request.method == 'POST':
		p = get_object_or_404(Project,id=object_id)
		
		p.check_manager(request.user, 'change')
		
		p.description = request.POST['content']
		p.save()
		
		return render(request,'project_description.html',{'object':p})

@login_required
def project_list(request):
	if request.user.is_staff:
		p = Project.objects.filter(active=True)
	else:
		p = request.user.projects_working.filter(active=True)
	return render(request,'project_list.html',{'object_list':p})
	
@login_required
def project_dashboard(request):
	my_proj = mergeLists(
						request.user.projects_working.filter(active=True).order_by("end_date"), 						
						request.user.projects_managed.filter(active=True).order_by("end_date")
				)
	
	my_task = [ [item, dist(item.due_date)] for item in request.user.actionitem_todo.filter(done=False) ]
	
	jk_proj = Project.objects.filter(active=True)

	late_projects = Project.objects.filter(active=True, end_date__lt=date.today())
	
	
	class MockUserWithCount(object):
		def __init__(self,user,count):
			self.user = user
			self.count = int(count)
	
	late_people = []
	for u in User.objects.all():
		c = u.actionitem_todo.filter(done=False,due_date__lt=date.today()).count()
		if c > 0:
			late_people.append(MockUserWithCount(u,c))
	late_people.sort(lambda x,y: y.count - x.count)
	
	late_tasks = ActionItem.objects.filter(done=False,due_date__lt=date.today())
	
	return render(request,'project_dashboard.html',{
				'my_proj_list':my_proj,
				'my_task_list':my_task,
				'jk_proj_list':jk_proj,
				'late_projects':late_projects,
				'late_people':late_people,
				'late_tasks':late_tasks
			})

@login_required
def project_detail(request,object_id):
	p = get_object_or_404(Project,id=object_id)
	p.check_user(request.user)
	
	return render(request,'project_detail.html',{
		'object':p,
		'notes': p.note_set.order_by("-set_date"),
		'files': p.file_set.order_by("-set_date"),
		'actionitems': [ [item, dist(item.due_date)] for item in p.actionitem_set.all() ]
		})

@login_required
def project_reopen(request, object_id):
	p = get_object_or_404(Project,id=object_id)
	p.check_manager(request.user, 'change')

	p.active = True
	p.save()
	
	return HttpResponseRedirect(p.get_absolute_url())

@login_required
def project_close(request, object_id):
	p = get_object_or_404(Project,id=object_id)
	p.check_manager(request.user, 'change')
	
	p.active = False
	p.save()
	
	for el in p.actionitem_set.filter(done=False):
		el.done = True
		el.save()
	
	return HttpResponseRedirect(p.get_absolute_url())

# Note Views

@login_required
def note_detail(request,object_id):
	p = get_object_or_404(Note,id=object_id)
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


# Action Item Note Views

@login_required
def actionnote_detail(request,object_id):
	p = get_object_or_404(ActionNote,id=object_id)
	p.actionitem.project.check_user(request.user)
	return render(request,'actionnote_detail.html',{'object':p})

@login_required
def actionnote_delete(request,object_id):
	return delete_view(request,object_id,ActionNote)

@login_required
def actionnote_create(request,object_id):
	return create_view(request,object_id,ActionNoteForm,"note_edit.html")


@login_required
def actionnote_edit(request,object_id):
	return edit_view(request,object_id,ActionNoteForm,"note_edit.html")


# File Views

@login_required
def file_detail(request,object_id):
	p = get_object_or_404(File,id=object_id)
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
	p = get_object_or_404(ActionItem,id=object_id)
	p.project.check_user(request.user)
	add_note_form = ActionNoteForm(initial={'author':request.user.id,'actionitem':object_id })
	return render(request,'action_detail.html',{
										'object':p,
										'notes': p.actionnote_set.order_by("-set_date", "-id"),
										"add_note_form":add_note_form
									})

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

	if not (request.user.has_perm('gestor.change_actionitem') or obj.project.has_user(request.user)):
		raise PermissionDenied()
	
	obj.done = True
	obj.save()
	return action_detail(request,object_id)
	
@login_required
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
		
		# TODO: escaping this stuff
		# vtodo.add('description').value = actionitem.description
		
		vtodo.add('due;value=date').value = actionitem.due_date.strftime("%Y%m%d")
		vtodo.add('priority').value = "0"
		
	
	icalstream = cal.serialize()
	response = HttpResponse(icalstream, mimetype='text/calendar')
	response['Filename'] = filename  # IE needs this
	response['Content-Disposition'] = 'attachment; filename='+filename
	return response

# Feed View

@login_required
def protected_feed(*args, **kwargs):
	return feed(*args, **kwargs)
	
@login_required
def search_everything(request):
	res = {}
	
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			search_term = form.cleaned_data['find'].rstrip()
			
			res['Cv'] = CurriculumVitae.objects.select_related("owner").filter(
									   Q(owner__first_name__icontains=search_term) \
									 | Q(owner__last_name__icontains=search_term) \
									 | Q(course__icontains=search_term) \
									 | Q(complements__icontains=search_term)    \
									 | Q(proficient_areas__icontains=search_term) \
									 | Q(foreign_langs__icontains=search_term) \
									 | Q(computer_skills__icontains=search_term) \
									 | Q(other_skills__icontains=search_term) \
									 | Q(interests__icontains=search_term) )

			res['User'] = list( set( list( User.objects.filter(
									   Q(first_name__icontains=search_term) \
									 | Q(last_name__icontains=search_term) \
									 | Q(username__icontains=search_term) ) ) \
						+ [ p.user for p in UserProfile.objects.filter(
									   Q(organization__icontains=search_term) \
									 | Q(title__icontains=search_term) \
									 | Q(description__icontains=search_term) ) ] ) )
									 
			
			res['Proj'] = Project.objects.filter(
									   Q(name__icontains=search_term) \
									 | Q(description__icontains=search_term) )
			
			res['ActionItem'] = ActionItem.objects.filter(
									   Q(title__icontains=search_term) \
									 | Q(description__icontains=search_term) )
			
			res['ActionNote'] = ActionNote.objects.filter(
									   Q(actionitem__title__icontains=search_term) \
									 | Q(description__icontains=search_term) )
			
			res['Note'] = Note.objects.filter(
									   Q(title__icontains=search_term) \
									 | Q(description__icontains=search_term) )
			
			res['File'] = File.objects.filter( Q(title__icontains=search_term) )
		
		else:
			return render(request,'generic_search.html',{'form':form,'results': False})
	else:
		form = SearchForm()
		return render(request,'generic_search.html',{'form':form,'results': False})
	
	return render(request,'generic_search.html',{'form':form,'results': len( [ v for k,v in res.items() if v ] ) > 0,
												  'res_cv': res['Cv'],
												  'res_user': res['User'],
												  'res_proj': res['Proj'],
												  'res_actionitem': res['ActionItem'],
												  'res_actionnote': res['ActionNote'],
												  'res_file': res['File'],
												  'res_note': res['Note'] })
