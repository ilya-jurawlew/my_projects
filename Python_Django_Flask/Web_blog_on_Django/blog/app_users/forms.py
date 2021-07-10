# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    city = forms.CharField(help_text=_('City'), max_length=50)
    avatar = forms.ImageField(help_text=_('Avatar'), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'city', 'password1', 'password2', ]


class EditRegisterForm(UserChangeForm):
    city = forms.CharField(required=False, help_text=_('City'))
    avatar = forms.FileField(required=False, help_text=_('Avatar'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'city', 'avatar', )


class RestorePasswordForm(forms.Form):
    email = forms.EmailField()
