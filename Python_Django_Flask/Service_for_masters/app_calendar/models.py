from django.db import models

from app_masters.models import UserProfile


class Calendar(models.Model):
    """Календарь мастера"""
    master = models.OneToOneField(UserProfile)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''


class DatesTimesCalendar(models.Model):
    """Время мастера"""
    TIME_STATUS_CHOICES = (
        ('', 'свободно'),
        ('', 'занято')
    )
    time = models.DateTimeField(verbose_name='', blank=False)
    status = models.CharField(verbose_name='', max_length=50, blank=False, default='', choices=TIME_STATUS_CHOICES)
    calendar = models.ForeignKey(Calendar, verbose_name='', on_delete=models.CASCADE, related_name='')

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'{self.time}'


class Meetings(models.Model):
    """Модель встречи мастера с клиентом"""
    date_time = models.DateTimeField(verbose_name='', blank=False)
    comment = models.CharField(verbose_name='', max_length=100, blank=True)
    example_photo = models.ImageField(verbose_name='', upload_to='', blank=True)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'{self.date_time} {self.comment}'
