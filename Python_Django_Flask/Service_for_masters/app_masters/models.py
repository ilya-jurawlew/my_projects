from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    """Профиль пользователя"""
    STATUS_CHOICES = (
        ('m', 'я мастер'),
        ('c', 'ищу мастера'),
    )
    email = models.EmailField(verbose_name='', max_length=40, blank=False, unique=True)
    password = models.CharField(verbose_name='', max_length=30, blank=False)

    status = models.CharField(verbose_name='', max_length=50, blank=False, default='', choices=STATUS_CHOICES)
    first_name = models.CharField(verbose_name='', max_length=20, blank=False)
    last_name = models.CharField(verbose_name='', max_length=20, blank=False)
    address = models.CharField(verbose_name='', max_length=150, blank=True)
    photo = models.ImageField(verbose_name='', upload_to='')
    experience = models.CharField(verbose_name='', max_length=20, blank=True)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'{self.id} {self.email} {self.first_name} {self.last_name} {self.address} {self.experience}'


class RatingStar(models.Model):
    """Звёзды рейтинга"""
    value = models.SmallIntegerField(verbose_name='', default=0)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ['-value']

    def __str__(self):
        return f'{self.value}'


class Rating(models.Model):
    """Рейтинг мастера"""
    client = models.ForeignKey(UserProfile, verbose_name='', on_delete=models.CASCADE, related_name='')
    star = models.ForeignKey(RatingStar, verbose_name='', on_delete=models.CASCADE, related_name='')
    master = models.ForeignKey(UserProfile, verbose_name='', on_delete=models.CASCADE, related_name='')

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'{self.star}'


class CategoryMaster(models.Model):
    """Категория мастера"""
    CATEGORY_CHOICES = (
        ('', 'мастер маникюра'),
        ('', 'мастер-бровист'),
        ('', 'мастер педикюра'),
        ('', 'лэшмейкер (наращивание ресниц)'),
    )
    title = models.CharField(verbose_name='', max_length=50, blank=True, default='', choices=CATEGORY_CHOICES)
    master = models.ForeignKey(UserProfile, verbose_name='', on_delete=models.CASCADE, related_name='')

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'{self.title}'


class ImagesWorkMaster(models.Model):
    """Фото работ мастера"""
    image = models.FileField(verbose_name='', upload_to='', blank=False)
    master = models.ForeignKey(UserProfile)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''


class Reviews(models.Model):
    """Отзывы о работе"""
    client = models.ForeignKey(UserProfile, verbose_name='', on_delete=models.CASCADE, related_name='')
    master = models.ForeignKey(UserProfile, verbose_name='', on_delete=models.CASCADE, related_name='')
    text = models.CharField(verbose_name='', max_length=30, blank=False)
    date_time = models.DateField(verbose_name='', auto_now_add=True, blank=False)
    image = models.ImageField(verbose_name='', upload_to='', blank=True)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'{self.text} {self.date_time}'
