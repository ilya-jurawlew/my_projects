from django.urls import path

from app_animals.views import AnimalsList, AnimalDetail, AnimalCreate, AnimalUpdate


app_name = 'app_animals'

urlpatterns = [
    path('', AnimalsList.as_view(), name='animal_list'),
    path('<int:id>', AnimalDetail.as_view(), name='animal_detail'),
    path('create', AnimalCreate.as_view(), name='animal_create'),
    path('<int:id>/update', AnimalUpdate.as_view(), name='animal_update'),
]