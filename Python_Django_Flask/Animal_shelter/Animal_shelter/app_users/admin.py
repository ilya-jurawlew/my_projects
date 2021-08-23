from django.contrib import admin

from app_users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'city', 'phone', 'shelter']


admin.site.register(Profile, ProfileAdmin)
