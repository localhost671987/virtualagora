from pyexpat import model
from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.urls import reverse


class Theme(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
    post_types = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    theme = models.ManyToManyField(
        Theme, blank=True, related_name='post_theme')
    title = models.CharField(max_length=250)
    description = models.TextField(null=True)
    published_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(
        max_length=15, choices=post_types, default='published', null=True, blank=True)
    image = models.ImageField(upload_to='post/', null=True, blank=True)
    image_caption = models.CharField(max_length=250, null=True, blank=True)
    objects = models.Manager()  # default manager
    post_objects = PostObjects()  # custom manager

    class Meta:
        ordering = ('-published_date',
                    )

    def __str__(self):
        return self.title

    def themes(self):
        return ', '.join([item.name for item in self.theme.all()])

    def get_absolute_url(self):
        return reverse('virtual_agora_app:post_detail' , args=[self.pk])
    
    def get_comments(self):
        return Comment.objects.filter(post=self).order_by('-published_date')


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=500)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('published_date',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.post)

    def children(self):
        return Comment.objects.filter(parent=self)


class Philosopher(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='philosopher/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('virtual_agora_app:philosopher_detail' , args=[self.pk])


class Quote(models.Model):
    title = models.TextField(max_length=500)
    author = models.ForeignKey(
        Philosopher, on_delete=models.CASCADE, related_name='quotes')
    theme = models.ManyToManyField(Theme, default=None)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.quote

    def themes(self):
        return ', '.join([item.name for item in self.theme.all()])


class Newsletter(models.Model):
    title = models.CharField(max_length=50)
    quotes = models.ManyToManyField(Quote, default=None)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    quote = models.ForeignKey(
        Quote, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(default=0)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.post, self.rating)


class MoodInstance(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='moodInstance')
    mood = models.CharField(max_length=50)
    theme = models.ForeignKey(
        Theme, on_delete=models.CASCADE, related_name='moods')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.mood)
