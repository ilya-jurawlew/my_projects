# -*- coding: utf-8 -*-
import csv

from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.shortcuts import redirect
from django.views import generic

from .forms import NewsForm, NewsFileForm, CommentsForm
from .models import News, ImagesNews


class NewsListView(generic.ListView):
    model = News
    template_name = 'app_news/news_list.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        tag = F('tag')
        if 'tag' in self.request.GET:
            tag = self.request.GET['tag']
        return News.objects.filter(activity=True, tag=tag).order_by('-created_at')


class NewsFileCreateView(generic.CreateView):
    model = News
    template_name = 'app_news/news_create.html'
    form_class = NewsFileForm

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('app_news.approved_news'):
            raise PermissionDenied
        else:
            file = request.FILES['many_news']
            many_news_file = csv.reader(file.read().decode('utf-8').split('\n'))
            for row in many_news_file:
                News.objects.filter(content=row[0]).create(created_at=row[1])
            return redirect('/news')


class NewsCreateView(generic.CreateView):
    model = News
    template_name = 'app_news/news_create.html'
    form_class = NewsForm

    def post(self, request, *args, **kwargs):
        form_class = NewsForm(request.POST, request.FILES)
        if not request.user.has_perm('app_news.approved_news'):
            raise PermissionDenied
        else:
            files = request.FILES.getlist('images')
            form_class.instance.activity = True
            form_class.save()
            for file in files:
                instance = ImagesNews(news=form_class.instance, image=file)
                instance.save()
            return redirect('/news')


class NewsEditView(generic.UpdateView):
    model = News
    template_name = 'app_news/news_edit.html'
    pk_url_kwarg = 'id'
    form_class = NewsForm

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        form_class = NewsForm(request.POST, request.FILES)
        if not request.user.has_perm('app_news.approved_news'):
            raise PermissionDenied
        else:
            files = request.FILES.getlist('images')
            form_class.instance.activity = True
            ImagesNews.objects.filter(news=self.get_object()).delete()
            for file in files:
                ImagesNews.objects.create(news=self.get_object(), image=file)
            return redirect('/news')


class NewsDetailView(generic.DetailView):
    template_name = 'app_news/news_detail.html'
    model = News
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_form = CommentsForm()
        context['comment_form'] = comment_form
        context['images'] = ImagesNews.objects.filter(news=self.get_object())
        print(context['images'])
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentsForm(request.POST)
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        if comment_form.is_valid():
            comment_form.instance.news = self.object
            comment_form.instance.user_id = request.user.id
            comment_form.save()
        else:
            context['comment_form'] = comment_form
            context['user'] = request.user.id
        return self.render_to_response(context)