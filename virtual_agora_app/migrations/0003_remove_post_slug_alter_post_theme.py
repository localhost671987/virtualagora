# Generated by Django 4.1 on 2022-09-03 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_agora_app', '0002_philosopher_image_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
        migrations.AlterField(
            model_name='post',
            name='theme',
            field=models.ManyToManyField(blank=True, related_name='post_theme', to='virtual_agora_app.theme'),
        ),
    ]
