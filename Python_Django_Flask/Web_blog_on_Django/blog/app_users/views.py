# -*- coding: utf-8 -*-

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.utils.translation import gettext as _

from Python_Django_Flask.Web_blog_on_Django.blog.app_users.models import Profile
from Python_Django_Flask.Web_blog_on_Django.blog.app_users.forms import RegisterForm, EditRegisterForm, RestorePasswordForm


class MyLogin(LoginView):
    template_name = 'app_users/login.html'


class MyLogoutView(LogoutView):
    template_name = 'app_users/logout.html'


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            city = form.cleaned_data.get('city')
            context = {'user': user, 'city': city}
            if request.FILES.get('avatar'):
                context['avatar'] = request.FILES.get('avatar')
            Profile.objects.create(**context)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = authenticate(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect('/news')
    else:
        form = RegisterForm()
    return render(request, 'app_users/register.html', {'form': form})


def restore_password(request):
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            new_password = User.objects.make_random_password()
            user_email = form.cleaned_data['email']
            current_user = User.objects.filter(email=user_email).first()
            if current_user:
                current_user.set_password(new_password)
                current_user.save()
            send_mail(
                subject=_('Password recovery'),
                message=_('Recovery'),
                from_email='admin.admin@mail.ru',
                recipient_list=[form.cleaned_data['email']]
            )
            return HttpResponse(_('Letter sent'))
    restore_password_form = RestorePasswordForm()
    context = {
        'form': restore_password_form
    }
    return render(request, 'app_users/restore_password.html', context=context)


class UserEditView(generic.UpdateView):
    model = Profile
    template_name = 'app_users/user_edit.html'
    pk_url_kwarg = 'id'
    form_class = EditRegisterForm
    success_url = '/news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_class = EditRegisterForm(instance=self.request.user)
        context['form_class'] = form_class
        return context

    def post(self, request, *args, **kwargs):
        user_form = EditRegisterForm(request.POST, request.FILES, instance=request.user)
        user = User.objects.get(pk=request.user.id)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        super().post(request, *args, **kwargs)
        return super().form_valid(user_form)


class ProfileDetailView(generic.DetailView):
    template_name = 'app_users/user_detail.html'
    model = Profile
    pk_url_kwarg = 'id'
