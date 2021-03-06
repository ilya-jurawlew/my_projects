# Generated by Django 3.2.6 on 2021-08-20 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shelter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Приют',
                'verbose_name_plural': 'Приюты',
            },
        ),
        migrations.CreateModel(
            name='Animals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.CharField(max_length=100)),
                ('date_arrival', models.DateField()),
                ('weight', models.CharField(max_length=5)),
                ('growth', models.CharField(max_length=5)),
                ('signs', models.CharField(max_length=100)),
                ('shelter', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='shelter', to='app_animals.shelter')),
            ],
            options={
                'verbose_name': 'Животное',
                'verbose_name_plural': 'Животные',
            },
        ),
    ]
