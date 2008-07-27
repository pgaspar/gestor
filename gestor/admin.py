from gestor.models import Project, ActionItem, Note
from django.contrib import admin

class ProjectAdmin(admin.ModelAdmin):	
	list_filter = ('active','manager','team','start_date','end_date',)
	search_fields = ['name','description']

admin.site.register(Project,ProjectAdmin)

class ActionItemAdmin(admin.ModelAdmin):	
	list_filter = ('project','done','targets',)
	search_fields = ['title','description','project']


admin.site.register(ActionItem,ActionItemAdmin)

class NoteAdmin(admin.ModelAdmin):	
	list_filter = ('project','author',)
	search_fields = ['title','description','project']


admin.site.register(Note,NoteAdmin)