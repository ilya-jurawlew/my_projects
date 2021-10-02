from django.contrib import admin

from .models import Calendar


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    pass



