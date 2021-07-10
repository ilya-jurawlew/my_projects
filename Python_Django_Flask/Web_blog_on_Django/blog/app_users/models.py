# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(verbose_name=_('City'), max_length=50, blank=True, null=True)
    avatar = models.FileField(verbose_name=_('Avatar'), upload_to='files/avatars/', blank=True, null=True)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return f'{self.id} {self.user} {self.city}'
