from django.urls import path

from app_note.views import ListNotes, CreateNote, DetailNote

app_name = 'app_note'

urlpatterns = [
    path('', ListNotes.as_view(), name='list_notes'),
    path('create', CreateNote.as_view(), name='create_note'),
    path('<int:pk>', DetailNote.as_view(), name='detail_note'),
]
