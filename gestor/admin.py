from gestor.models import Project, ActionItem, Note, ActionNote
from django.contrib import admin

class ProjectAdmin(admin.ModelAdmin):	
	list_display = ('name','manager','active','start_date','end_date',)	
	list_filter = ('active','manager','team','start_date','end_date',)
	search_fields = ['name','description']

try: admin.site.register(Project,ProjectAdmin)
except: pass

class ActionItemAdmin(admin.ModelAdmin):	
	list_display = ('title','project','done','due_date','priority')
	list_filter = ('project','done','targets','priority')
	search_fields = ['title','description','project']
	ordering = ('-due_date',)


try: admin.site.register(ActionItem,ActionItemAdmin)
except: pass

class NoteAdmin(admin.ModelAdmin):	
	list_display = ('title','project','author',)
	list_filter = ('project','author',)
	search_fields = ['title','description','project']


try: admin.site.register(Note,NoteAdmin)
except: pass

class ActionNoteAdmin(admin.ModelAdmin):	
	list_display = ('actionitem','author',)
	list_filter = ('actionitem','author',)
	search_fields = ['description','actionitem']


try: admin.site.register(ActionNote,ActionNoteAdmin)
except: pass
