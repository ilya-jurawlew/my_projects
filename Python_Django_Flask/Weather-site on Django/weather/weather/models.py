from django.db import models


class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return {self.id}
