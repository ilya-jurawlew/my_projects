from django import forms

from app_note.models import Note


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['title', 'text']
