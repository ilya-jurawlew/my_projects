from django.contrib.auth.decorators import permission_required
from django.urls import path

from .views import NewsListView, NewsCreateView, NewsEditView, NewsDetailView, NewsFileCreateView

app_name = 'app_news'

urlpatterns = [
    path('', NewsListView.as_view(), name='list'),
    path('create', permission_required('app_news.create_and_edit_news', login_url='create',
                                       raise_exception=True)(NewsCreateView.as_view()), name='create'),
    path('many_create', permission_required('app_news.create_and_edit_news', login_url='many_create',
                                            raise_exception=True)(NewsFileCreateView.as_view()), name='many_create'),
    path('<int:id>/edit', permission_required('app_news.create_and_edit_news', login_url='edit',
                                              raise_exception=True)(NewsEditView.as_view()), name='edit'),
    path('<int:id>', NewsDetailView.as_view(), name='detail'),
]
