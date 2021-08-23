from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from app_users.models import Profile
from app_users.forms import RegisterForm
from django.views import generic


class MyLogin(LoginView):
    template_name = 'app_users/login.html'


class MyLogout(LogoutView):
    template_name = 'app_users/logout.html'


class UserDetail(generic.DetailView):
    model = Profile
    template_name = 'app_users/detail.html'
    pk_url_kwarg = 'id'


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            redirect('/animals')
    else:
        form = RegisterForm()
    return render(request, 'app_users/register.html', {'form': form})
