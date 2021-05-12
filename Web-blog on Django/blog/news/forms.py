from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

from .models import TableBd


class TableBdForm(ModelForm):
    class Meta:
        model = TableBd
        fields = ['title', 'anons', 'text', 'date']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название'
            }),
            'anons': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Анонс'
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Основной текст'
            }),
            'date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата публикации'
            }),
        }