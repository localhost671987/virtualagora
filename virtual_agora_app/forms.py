from django import forms
from .models import Post, Comment, Quote


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        description = forms.CharField(label='Description',
                                      widget=forms.Textarea(attrs={'class': 'ckeditor'}))

        exclude = ['author', 'published_date']


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'published_date', 'parent']


class QuoteCreateForm(forms.ModelForm):
    class Meta:
        model = Quote
        exclude = ['published_date']
