from django.contrib import admin

from .models import Comments, News


class CommentsInlane(admin.TabularInline):
    model = Comments
    extra = 0


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'normal_date', 'status']
    list_filter = ['status']
    inlines = [CommentsInlane]

    actions = ['mark_as_actively', 'mark_as_not_active']

    def normal_date(self, obj):
        return obj.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    def mark_as_actively(self, request, queryset):
        queryset.update(status='a')

    def mark_as_not_active(self, request, queryset):
        queryset.update(status='n')

    mark_as_actively.short_description = 'Перевести в статус Активно'
    mark_as_not_active.short_description = 'Перевести в статус Неактивно'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'short_text']
    list_filter = ['user']

    actions = ['delete_message']

    def short_text(self, obj):
        if len(obj.text) > 15:
            return ("%s" % obj.text)[:15] + "..."
        else:
            return ("%s" % obj.text)

    def delete_message(self, request, queryset):
        queryset.update(text='Сообщение удалено администратором')

    delete_message.short_description = 'Удалить комментарий'


admin.site.register(News, NewsAdmin)
admin.site.register(Comments, CommentsAdmin)