from cvmanager.models import CurriculumVitae
from django.contrib import admin

class CurriculumVitaeAdmin(admin.ModelAdmin):	
	list_display = ('owner','course','course_year','set_date',)	
	list_filter = ('owner','course','course_year','set_date')
	search_fields = ('owner','course')

try: admin.site.register(CurriculumVitae,CurriculumVitaeAdmin)
except: pass