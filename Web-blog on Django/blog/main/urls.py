from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name='home_page'),
    path('about/', views.about, name='about'),
]