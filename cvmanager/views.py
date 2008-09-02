from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template.context import RequestContext
from cvmanager.models import CurriculumVitae

from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import *
from django.forms import *
from cvmanager.forms import CvFrom



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

def curriculum(request,username):
    u = get_object_or_404(User, username = username)
    c = get_object_or_404(CurriculumVitae, owner = u)
    return render(request,'curriculum.html',{'u':u, 'cv':c})

@login_required
def curriculum_create(request,object_id):
    return create_view(request,object_id,CvForm,'curriculum_edit.html')

    
@login_required
def curriculum_edit(request,object_id):
    return edit_view(request,object_id,CvForm,'curriculum_edit.html')

