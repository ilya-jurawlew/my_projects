from django.shortcuts import redirect
from django.views import generic

from app_animals.models import Animals
from app_animals.forms import AnimalForm


class AnimalsList(generic.ListView):
    model = Animals
    template_name = 'app_animals/animal_list.html'
    context_object_name = 'animals'


class AnimalDetail(generic.DetailView):
    model = Animals
    template_name = 'app_animals/animal_detail.html'
    pk_url_kwarg = 'id'


class AnimalCreate(generic.CreateView):
    model = Animals
    template_name = 'app_animals/animal_create.html'
    form_class = AnimalForm

    def post(self, request, *args, **kwargs):
        form_class = AnimalForm(request.POST)
        form_class.save()
        return redirect('/animals')


class AnimalUpdate(generic.UpdateView):
    model = Animals
    template_name = 'app_animals/animal_update.html'
    pk_url_kwarg = 'id'
    form_class = AnimalForm
