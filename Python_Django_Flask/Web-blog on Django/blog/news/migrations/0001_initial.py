# Generated by Django 3.1.1 on 2020-11-26 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TableBd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('anons', models.CharField(max_length=250, verbose_name='Анонс')),
                ('text', models.TextField(verbose_name='Текст статьи')),
                ('date', models.DateTimeField(verbose_name='Дата публикации')),
            ],
        ),
    ]