from django.contrib import admin
from .models import Theme, Post, Comment, Rating, Newsletter, Quote, Philosopher, MoodInstance
from django import forms

admin.site.register(Theme)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Newsletter)
admin.site.register(Quote)
admin.site.register(Philosopher)
admin.site.register(MoodInstance)
