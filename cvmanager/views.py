from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template.context import RequestContext
from cvmanager.models import CurriculumVitae

def curriculum(request,username):
    u = get_object_or_404(User, username = username)
    c = get_object_or_404(CurriculumVitae, owner = u)
    return render(request,'curriculum.html',{'u':u, 'cv':c})