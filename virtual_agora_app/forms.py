from django import forms
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'published_date']


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'published_date', 'parent']
