from formacao.models import Event
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):	
	list_display = ('name','date','eventType')	
	list_filter = ('date','eventType')
	search_fields = ['name','content']
	ordering = ('date',)

admin.site.register(Event, EventAdmin)
