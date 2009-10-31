from activitystream.models import *
from django.contrib import admin

class ActivityModel(admin.ModelAdmin):
	search_fields = ['message']

admin.site.register(Activity, ActivityModel)