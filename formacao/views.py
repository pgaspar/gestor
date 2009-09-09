from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from common.utils import render

from django.core.exceptions import PermissionDenied

from formacao.models import Event

def view_content_with_slug(request, slug):
	event = get_object_or_404(Event, slug=slug)
	
	if (not event.is_published or event.is_short_preview) and not request.user.has_perms('formacao.event.can_change'):
		raise Http404
	else:
		return render(request,'event_detail.html',{'event':event})

def view_content(request, object_id):
	event = get_object_or_404(Event, id=object_id)
	
	if (not event.is_published or event.is_short_preview) and not request.user.has_perms('formacao.event.can_change'):
		raise Http404
	else:
		return render(request,'event_detail.html',{'event':event})

def view_private_content(request, object_id):
	event = get_object_or_404(Event, id=object_id)
	
	if (not event.is_published or event.is_short_preview) and not request.user.has_perms('formacao.event.can_change'):
		raise Http404
	else:
		if request.user.has_perms('formacao.event.can_change') or \
		  (request.method == 'POST' and request.POST['pwd'] == event.password) or \
		  (event.privateContent and not event.password):
		  
			return render(request,'event_detail.html',{'event':event, 'private':True})
   
		else:
			return HttpResponseRedirect(event.get_absolute_url())
	
def surveys(request, object_id, register):
	event = get_object_or_404(Event, id=object_id)
	
	if (not event.is_published or event.is_short_preview) and not request.user.has_perms('formacao.event.can_change'):
		raise Http404
	else:
		if register: url = event.iframeUrl_registration
		else: url = event.iframeUrl_surveys
		
		if url and not (register and event.close_registration):
			return render(request,'survey_template.html',{'iFrameUrl':url, 'event':event})
		else:
			raise Http404

def surv_response(request, object_id):
	event = get_object_or_404(Event, id=object_id)
	if event.confirmBox: return render(request,'survey_response.html', {'event':event})
	else: return HttpResponseRedirect('/formacao/thanks/')
	