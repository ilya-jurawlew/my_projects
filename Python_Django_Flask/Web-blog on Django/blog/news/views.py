from django.shortcuts import render, redirect
from django.views.generic import DetailView, DeleteView, UpdateView, ListView

from .models import TableBd

from .forms import TableBdForm


def news_home(request):
    news = TableBd.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})


class NewDetailView(DetailView):
    model = TableBd
    template_name = 'news/detail_view.html'
    context_object_name = 'table'


class NewUpdateView(UpdateView):
    model = TableBd
    template_name = 'news/create.html'
    form_class = TableBdForm


class NewDeleteView(DeleteView):
    model = TableBd
    success_url = '/news'
    template_name = 'news/news_delete.html'


def create(request):
    error = ''
    if request.method == 'POST':
        form = TableBdForm(request.POST) # передаём созданную форму
        if form.is_valid(): # проверка корректности заполненных данных
            form.save()
            return redirect('news_home')
        else:
            error = 'Ошибка записи'

    form = TableBdForm()
    data = {
        'form': form, 'error': error
    }
    return render(request, 'news/create.html', data)
