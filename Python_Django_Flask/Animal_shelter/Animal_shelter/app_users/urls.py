from django.urls import path

from app_users.views import MyLogin, MyLogout, UserDetail, RegisterUser


app_name = 'app_users'

urlpatterns = [
    path('login', MyLogin.as_view(), name='login'),
    path('logout', MyLogout.as_view(), name='logout'),
    path('register', RegisterUser.as_view(), name='register'),
    path('<int:id>', UserDetail.as_view(), name='user_detail'),
]