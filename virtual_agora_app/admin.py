from django.contrib import admin
from .models import Theme, Post, Comment, Rating, Newsletter, Quote, Philosopher
# Register your models here.
admin.site.register(Theme)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Newsletter)
admin.site.register(Quote)
admin.site.register(Philosopher)