from activitystream.models import Activity
from activitystream.forms import ActivityMessageForm

from settings import *
from common.utils import render
from common.views import PermissionDenied
from django.shortcuts import get_object_or_404

def activity_stream(request, all):
    
    if not request.user.has_perm('activitystream.view_everything'): return PermissionDenied(request)

    NUM_OF_ACTIVITIES = 20
    
    if request.method == 'POST' and request.user.has_perm('activitystream.add_activity'):
        
        form = ActivityMessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            activity = Activity(message_type = Activity.MSG_USER, message = message)
            activity.save()
    else:
        form = ActivityMessageForm()
    
    if all:
        activities = Activity.objects.all()
    else:
        activities = Activity.objects.all()[:NUM_OF_ACTIVITIES]
    return render(request,'activity_stream.html',{'activities':activities, 'form':form, 'all':all})

def activity_stream_detail(request, stream_id):
    activity = get_object_or_404(Activity, id=stream_id)
    return render(request,'activity_stream_detail.html',{'object':activity})
    