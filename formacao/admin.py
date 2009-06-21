from formacao.models import Event
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):	
	list_display = ('name','date','eventType','is_published','is_short_preview')	
	list_filter = ('date','eventType')
	search_fields = ['name','content']
	ordering = ('date',)

admin.site.register(Event, EventAdmin)
