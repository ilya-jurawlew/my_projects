from django.db import models

from app_user.models import Profile
from django.urls import reverse


class Note(models.Model):
    """"""

    title = models.CharField(max_length=50, blank=True, default=' ')
    text = models.TextField(max_length=10000, blank=True, default=' ')
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    user = models.ForeignKey(Profile, default=None, null=True, blank=False, on_delete=models.CASCADE, related_name='user_notes')

    class Meta:
        verbose_name = 'note'
        verbose_name_plural = 'notes'

    def __str__(self):
        return f'{self.id} {self.title} {self.text}'

    def get_absolute_url(self):
        return reverse('app_note:detail_note', args=[self.id])
