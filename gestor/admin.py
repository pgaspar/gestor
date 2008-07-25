from gestor.models import Project, ActionItem, Note
from django.contrib import admin

class ProjectAdmin(admin.ModelAdmin):
	
	list_filter = ('status','manager','workers','start_date','end_date',)
	search_fields = ['name','description']

admin.site.register(Project,ProjectAdmin)


admin.site.register(ActionItem)

admin.site.register(Note)