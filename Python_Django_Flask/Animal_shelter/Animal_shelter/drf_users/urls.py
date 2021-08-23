from django.urls import path

from drf_users.views import ListUsersAPI, DetailUserAPI, RegisterUserAPI, LoginAPI


app_name = 'app_users_animals'

urlpatterns = [
    path('', ListUsersAPI.as_view(), name='list_users'),
    path('<int:id>', DetailUserAPI.as_view(), name='detail_user'),
    path('register/', RegisterUserAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(),  name='login'),
]