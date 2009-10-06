from django.http import HttpResponseForbidden
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

@login_required
def PermissionDenied(request):
	t = loader.get_template('403.html')
	return HttpResponseForbidden(t.render(RequestContext(request)))