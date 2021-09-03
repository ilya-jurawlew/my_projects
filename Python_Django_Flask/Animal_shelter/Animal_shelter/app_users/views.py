from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect

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


class RegisterUser(generic.CreateView):
    template_name = 'app_users/register.html'
    form_class = RegisterForm

    def post(self, request, *args, **kwargs):
        form_class = RegisterForm(request.POST)
        if form_class.is_valid():
            user = form_class.save()
            login(request, user)
        super().post(request, *args, **kwargs)
        return redirect('app_animals:animal_list')
