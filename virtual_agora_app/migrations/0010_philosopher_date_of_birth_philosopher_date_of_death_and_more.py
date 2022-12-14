# Generated by Django 4.1 on 2022-09-08 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('virtual_agora_app', '0009_comment_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='philosopher',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='philosopher',
            name='date_of_death',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='philosopher',
            name='link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_post', to='virtual_agora_app.post'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='quote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_quote', to='virtual_agora_app.quote'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='theme',
            field=models.ManyToManyField(blank=True, default=None, to='virtual_agora_app.theme'),
        ),
    ]
