from django.urls import path

from app_users.views import MyLogoutView, MyLogin, register_user, restore_password, UserEditView, ProfileDetailView

app_name = 'app_users'


urlpatterns = [
    path('login/', MyLogin.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', register_user, name='register'),
    path('restore_password/', restore_password, name='restore_password'),
    path('<int:id>/edit', UserEditView.as_view(), name='edit'),
    path('<int:id>', ProfileDetailView.as_view(), name='detail'),
]
