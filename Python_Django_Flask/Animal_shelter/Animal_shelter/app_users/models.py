from django.contrib.auth.models import User, AbstractUser
from django.db import models

from app_animals.models import Shelter


class Profile(AbstractUser):
    username = models.CharField(max_length=150, blank=True, unique=True)
    password = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    shelter = models.ForeignKey(Shelter, blank=True, null=True, on_delete=models.CASCADE, related_name='user_in_shelter')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.id} {self.username} {self.city} {self.phone} {self.birthday} {self.shelter}'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
