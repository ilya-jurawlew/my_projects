from django.contrib import admin

from app_animals.models import Animals, Shelter


class AnimalsAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_arrival', 'shelter']


class ShelterAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Animals, AnimalsAdmin)
admin.site.register(Shelter, ShelterAdmin)
