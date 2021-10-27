from django.contrib import admin

from .models import MasterProfile, Rating, CategoryMaster, Reviews


@admin.register(MasterProfile)
class MasterProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryMaster)
class CategoryMasterAdmin(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    pass