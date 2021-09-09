from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.views import generic

from app_note.models import Note
from app_note.forms import NoteForm


class ListNotes(generic.ListView):
    model = Note
    template_name = 'app_note/list_notes.html'
    context_object_name = 'notes_list'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.user.is_authenticated():
    #         context['notes_list'] = Note.objects.filter(user=self.request.user).order_by('-created_at')
    #     return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Note.objects.filter(user=self.request.user).order_by('-created_at')


class CreateNote(generic.CreateView):
    model = Note
    template_name = 'app_note/create_notes.html'
    form_class = NoteForm
    success_url = '/note'

    def post(self, request, *args, **kwargs):
        form_class = NoteForm(request.POST)
        form_class.instance.user_id = request.user.id
        form_class.save()
        return super().form_valid(form_class)


class DetailNote(generic.UpdateView):
    model = Note
    template_name = 'app_note/detail_notes.html'
    form_class = NoteForm
    pk_url_kwarg = 'pk'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     form_class = NoteForm(instance=self.get_object())
    #     context['form_class'] = form_class
    #     return context

    def post(self, request, *args, **kwargs):
        form_class = NoteForm(request.POST, instance=self.get_object())
        super().post(request, *args, **kwargs)
        return super().form_valid(form_class)
