# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ImagesNews(models.Model):
    image = models.ImageField(verbose_name=_('Images'), upload_to='files/images/', blank=True)
    news = models.ForeignKey('News', null=True, default=None, blank=True, on_delete=models.CASCADE,
                             related_name='images_news', verbose_name='News')


class News(models.Model):
    active = _('active')
    not_active = _('not_active')
    STATUS_CHOICES = [
        (active, _('active')),
        (not_active, _('not_active')),
    ]
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE, blank=True,
                             related_name='user_news', verbose_name=_('User'))
    title = models.CharField(verbose_name=_('Name'), max_length=150, db_index=True, blank=True)
    content = models.CharField(verbose_name=_('Content'), max_length=1000)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True, blank=False)
    status = models.CharField(verbose_name=_('Status'), max_length=100, default='active', choices=STATUS_CHOICES, blank=True)
    activity = models.BooleanField(verbose_name=_('Permission to publish'), default=False, blank=True)
    tag = models.CharField(verbose_name=_('Tag'), max_length=50, default='', blank=True)
    many_news = models.FileField(verbose_name=_('File many news'), upload_to='files/file_news/', blank=True)

    class Meta:
        verbose_name = _('news')
        verbose_name_plural = _('news')
        permissions = (
            ('create_and_edit', _('create and edit')),
            ('approved', _('approved moderator'))
        )

    def __str__(self):
        return f'{self.id}. {self.title} {self.created_at}'

    def get_absolute_url(self):
        return reverse('app_news:detail', args=[self.pk])


class Comments(models.Model):
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE, blank=True,
                             related_name='user_comment', verbose_name=_('User'))
    nickname = models.CharField(max_length=50, default='', blank=True)
    text = models.CharField(verbose_name=_('Comment'), max_length=500)
    news = models.ForeignKey('News', null=True, default=None, blank=True, on_delete=models.CASCADE,
                             related_name='comments', verbose_name=_('News'))

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return f'{self.id} {self.user} {self.text}'
