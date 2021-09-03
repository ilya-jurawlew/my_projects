from django import forms

from .models import News, Comments


class NewsForm(forms.ModelForm):
    images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = News
        fields = '__all__'
        exclude = ['user', 'many_news']


class NewsFileForm(forms.ModelForm):
    many_news = forms.FileField()

    class Meta:
        model = News
        fields = ['many_news']


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'
