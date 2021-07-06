from rest_framework import generics
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend

from .models import News, Comments
from .serializers import NewsListSerializers, NewsDetailSerializers, CommentsCreateSerializers


# class NewsListView(APIView):
#     """Вывод списка новостей"""
#
#     def get(self, request):
#         news = News.objects.all()
#         serializer = NewsListSerializers(news, many=True) # сюда отрабатывает сериализатор
#         return Response(serializer.data) # возвращаем данные сериализатора (тут на выходе формат json)
#
#
# class NewsDetailView(APIView):
#     """Вывод деталей новости"""
#
#     def get(self, request, pk):
#         news = News.objects.get(id=pk)
#         serializer = NewsDetailSerializers(news)
#         return Response(serializer.data)

class CharFilterInFilter(rest_framework.BaseInFilter, rest_framework.CharFilter):
    pass


class NewsFilter(rest_framework.FilterSet):
    title = CharFilterInFilter(field_name='title__title', lookup_expr='in') # в поле title, in - показывает как ищем
    tag = rest_framework.RangeFilter() # потому что диапазон, доступ в урле /?year_min='int'&year_max='int'&title='str'

    class Meta:
        model = News
        fields = ['title', 'tag']


class NewsListView(generics.ListAPIView):
    """Вывод списка новостей (аналог и вьюхи 1) """

    queryset = News.objects.all()
    serializer_class = NewsListSerializers

    filter_backends = (DjangoFilterBackend,) # подключаем фильтрацию
    filterset_class = NewsFilter


class NewsDetailView(generics.RetrieveAPIView):
    """Вывод деталей новости (аналог вьюхи 2)"""

    queryset = News.objects.filter()
    serializer_class = NewsDetailSerializers


class CommentsCreateView(generics.CreateAPIView):
    """Создание комментариев"""

    serializer_class = CommentsCreateSerializers
