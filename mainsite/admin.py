from mainsite.models import News
from django.contrib import admin

class NewsAdmin(admin.ModelAdmin):	
	list_display = ('title','date','is_published')	
	list_filter = ('date',)
	search_fields = ['title','body']

admin.site.register(News, NewsAdmin)
