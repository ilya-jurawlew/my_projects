from django.urls import path

from app_user.views import MyLogin, RegisterUser, ChangePassword, RestorePassword


app_name = 'app_user'

urlpatterns = [
    path('login', MyLogin.as_view(), name='login'),
    path('register', RegisterUser.as_view(), name='register'),
    path('<int:id>/change-password', ChangePassword.as_view(), name='change_password'),
    path('restore-password', RestorePassword.as_view(), name='restore_password'),
]
