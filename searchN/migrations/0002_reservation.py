# Generated by Django 5.2.4 on 2025-07-12 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchN', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('number_of_people', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('comments', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
