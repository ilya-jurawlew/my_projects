from django.urls import path
from .import views


urlpatterns = [
    path('', views.index),
    path('<int:id>/delete', views.Delete.as_view(), name='delete'),
]
