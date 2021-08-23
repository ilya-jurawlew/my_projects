from django.db import models

from django.urls import reverse


class Animals(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    date_arrival = models.DateField()
    weight = models.CharField(max_length=5)
    growth = models.CharField(max_length=5)
    signs = models.CharField(max_length=100)
    shelter = models.ForeignKey('Shelter', blank=True, on_delete=models.CASCADE, related_name='shelter')

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'

    def __str__(self):
        return f'{self.id} {self.name}'

    def get_absolute_url(self):
        return reverse('app_animals:animal_detail', args=[self.pk])


class Shelter(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Приют'
        verbose_name_plural = 'Приюты'

    def __str__(self):
        return f'{self.id}. {self.name}'
