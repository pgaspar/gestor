from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http_404
from common.utils import render

from django.core.exceptions import PermissionDenied

from formacao.models import Event

def view_content(request, object_id):
	event = get_object_or_404(Event, id=object_id)
	
	if event.is_published == False:
		#if request.user.has_perms('posts.post.can_change') == False:
		return Http_404()

def view_private_content(request, object_id):
	event = get_object_or_404(Event, id=object_id)
	
	if request.method == 'POST':
		if request.POST['pwd'] == event.password:
			return render(request,'event_private_detail.html',{'event':event})
		else
			raise PermissionDenied()
	
	
	