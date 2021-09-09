from django.contrib import admin

from app_user.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']


admin.site.register(Profile, ProfileAdmin)
