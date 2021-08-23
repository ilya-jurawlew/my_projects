from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from app_animals.models import Animals
from drf_animals.serializers import AnimalsSerializers


class MyClassPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class AnimalsList(generics.ListCreateAPIView):
    """Список всех животных"""
    serializer_class = AnimalsSerializers
    pagination_class = MyClassPagination

    def get_queryset(self):
        queryset = Animals.objects.all()
        shelter = self.request.query_params.get('shelter')
        if shelter:
            queryset = queryset.filter(shelter=shelter)
        return queryset


class AnimalDetail(generics.RetrieveUpdateDestroyAPIView):
    """Детальный вывод животного"""
    queryset = Animals.objects.filter()
    serializer_class = AnimalsSerializers
