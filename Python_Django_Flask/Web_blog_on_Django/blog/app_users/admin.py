from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'avatar']
    list_filter = ['user']


admin.site.register(Profile, ProfileAdmin)
