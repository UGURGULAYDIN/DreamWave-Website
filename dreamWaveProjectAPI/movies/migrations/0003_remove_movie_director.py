# Generated by Django 5.2 on 2025-04-06 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_director_alter_movie_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='director',
        ),
    ]
