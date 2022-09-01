from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.views.generic.list import ListView

# Create your views here.


def index(request):
    return render(request, 'index.html')


class PostView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
