# Generated by Django 5.1.2 on 2024-12-03 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_moviereview'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviereview',
            name='title',
            field=models.TextField(default='Reseña sin titulo'),
        ),
    ]