from .models import Post, Philosopher, Comment
from django.utils import timezone
from users.forms import RegistrationForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostCreateForm, CommentCreateForm
from django.urls import reverse_lazy, reverse

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('email')
            # raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def index(request):
    return render(request, 'index.html')


class PostView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    paginate_by = 10


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    form_class = CommentCreateForm

    def get_success_url(self):
        return reverse('virtual_agora_app:post_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentCreateForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form.instance.author = self.request.user
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.post = self.object
        obj.save()
        return super(PostDetailView, self).form_valid(form)


class MyPostsView(ListView):
    model = Post
    template_name = 'my_posts.html'
    context_object_name = 'posts'

    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-published_date')


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def get_comment(self):
    return Comment.objects.filter(post=self.object).order_by('-created_date')


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('virtual_agora_app:post_list')
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('virtual_agora_app:post_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('virtual_agora_app:post_list')
        return super().dispatch(request, *args, **kwargs)


class AboutView(TemplateView):
    template_name = 'about.html'


class PhilosopherListView(ListView):
    model = Philosopher
    template_name = 'philosopher_list.html'
    context_object_name = 'philosophers'

    paginate_by = 10


class PhilosopherDetailView(DetailView):
    model = Philosopher
    template_name = 'philosopher_detail.html'
    context_object_name = 'philosopher'
