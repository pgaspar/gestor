from formacao.models import Event
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):	
	list_display = ('name','date','type')	
	list_filter = ('date','type')
	search_fields = ['name','content']

admin.site.register(Event, EventAdmin)
