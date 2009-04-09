from mainsite.models import News
from mainsite.forms import NewsForm

from django.contrib.auth.decorators import login_required
from common.utils import render
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import PermissionDenied

# News Views

@login_required
def create_news(request):
	if request.user.is_staff:
	
		if request.method == 'POST':
			form = NewsForm(request.POST)

			if form.is_valid():
				obj = form.save()

				request.user.message_set.create(message="News Created")

				return HttpResponseRedirect(obj.get_absolute_url())
		else:
			form = NewsForm()
		return render(request,"news_edit.html",{'form':form})

	else:
		raise PermissionDenied()

def index(request):
	latest = News.objects.order_by('-date')[:3]
	return render(request,'index.html', {'latest': latest})