from django.contrib.auth.forms import UserCreationForm
from django import forms

from app_users.models import Profile


class RegisterForm(UserCreationForm):
    birthday = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y',
                                                      attrs={'class': 'datepicker', 'placeholder': 'Select a date',
                                                             'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['username', 'city', 'phone', 'birthday', 'shelter']
