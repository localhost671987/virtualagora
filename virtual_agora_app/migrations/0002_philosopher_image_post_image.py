# Generated by Django 4.1 on 2022-09-03 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_agora_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='philosopher',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='philosopher/'),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post/'),
        ),
    ]
