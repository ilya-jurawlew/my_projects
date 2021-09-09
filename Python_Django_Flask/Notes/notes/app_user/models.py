from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.id} {self.first_name} {self.last_name} {self.email}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
