from django.contrib import admin

from Python_Django_Flask.Web_blog_on_Django.blog.app_users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'avatar']
    list_filter = ['user']


admin.site.register(Profile, ProfileAdmin)
