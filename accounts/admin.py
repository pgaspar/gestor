from accounts.models import UserProfile
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):	
	list_display = ('user','organization')	
	list_filter = ('organization',)
	search_fields = ('user','title')

admin.site.register(UserProfile,UserProfileAdmin)
