from django.urls import path

from .views import NewsListView, NewsDetailView, CommentsCreateView


urlpatterns = [
    path('news', NewsListView.as_view(), name='list'),
    path('news/<int:pk>', NewsDetailView.as_view(), name='detail'),
    path('comments', CommentsCreateView.as_view(), name='comments_create')
]
