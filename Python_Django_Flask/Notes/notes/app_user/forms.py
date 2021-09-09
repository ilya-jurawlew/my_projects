from django import forms

from app_user.models import Profile


class RegisterUserForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['email', 'password', 'first_name', 'last_name']


# class LoginForm(forms.Form):
#
#     email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
#     password = forms.CharField(
#         label='Password',
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
#     )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=50)
    new_password = forms.CharField(max_length=50)


class RestorePasswordForm(forms.Form):
    email = forms.EmailField()