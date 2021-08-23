from django.urls import path

from drf_animals.views import AnimalsList, AnimalDetail


app_name = 'app_drf_animals'

urlpatterns = [
    path('', AnimalsList.as_view(), name='animals_list'),
    path('<int:pk>', AnimalDetail.as_view(), name='animal_detail'),
]