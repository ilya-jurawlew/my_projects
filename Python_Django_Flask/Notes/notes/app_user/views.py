from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic

from app_user.forms import RegisterUserForm, RestorePasswordForm, ChangePasswordForm
from app_user.models import Profile


class MyLogin(LoginView):
    """"""
    template_name = 'app_user/login.html'


class RegisterUser(generic.CreateView):
    """"""
    template_name = 'app_user/register.html'
    form_class = RegisterUserForm

    def post(self, request, *args, **kwargs):
        form_class = RegisterUserForm(request.POST)
        if form_class.is_valid():
            user = form_class.save()
            login(request, user)
        super().post(request, *args, **kwargs)
        return redirect('app_note:list_notes')


class ChangePassword(generic.UpdateView):
    """"""
    model = Profile
    form_class = ChangePasswordForm
    template_name = 'app_user/update_password.html'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        form_class = ChangePasswordForm(request.POST)
        if form_class.is_valid():
            old_password = form_class.cleaned_data.get('old_password')
            new_password = form_class.cleaned_data.get('new_password')
            current_user = Profile.objects.filter(email=self.request.user.email, password=old_password).first()
            if current_user:
                current_user.password = new_password
                current_user.save()
            return HttpResponse('password change')


class RestorePassword(generic.UpdateView):
    model = Profile
    form_class = RestorePasswordForm
    template_name = 'app_users/change_password.html'
    pk_url_kwarg = 'id'

# def restore_password(request):
#     if request.method == 'POST':
#         form = RestorePasswordForm(request.POST)
#         if form.is_valid():
#             new_password = User.objects.make_random_password()
#             user_email = form.cleaned_data['email']
#             current_user = User.objects.filter(email=user_email).first()
#             if current_user:
#                 current_user.set_password(new_password)
#                 current_user.save()
#             send_mail(
#                 subject=_('Password recovery'),
#                 message=_('Recovery'),
#                 from_email='admin.admin@mail.ru',
#                 recipient_list=[form.cleaned_data['email']]
#             )
#             return HttpResponse(_('Letter sent'))
#     restore_password_form = RestorePasswordForm()
#     context = {
#         'form': restore_password_form
#     }
#     return render(request, 'app_users/restore_password.html', context=context)

