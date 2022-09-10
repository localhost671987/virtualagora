from .models import MoodInstance, Post, Philosopher, Comment, Quote, Theme
from users.models import CustomUser as User
from django.utils import timezone
from users.forms import RegistrationForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostCreateForm, CommentCreateForm, QuoteCreateForm, SubmitMoodForm
from django.urls import reverse_lazy, reverse
import text2emotion as te
import nltk
nltk.download('omw-1.4')

# Create your views here.


def get_emotion_list(text):
    dict = te.get_emotion(text)
    emotions = [item for item in dict if dict[item] > 0.3]
    return Theme.objects.filter(name__in=emotions)


def get_emotion_max(text):
    dict = te.get_emotion(text)
    if max(dict.values()) > 0:
        emotion = max(dict, key=dict.get)
        return Theme.objects.get(name=emotion)
    else:
        return None


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
    if request.method == 'POST':
        form = SubmitMoodForm(request.POST)
        if form.is_valid():
            mood = form.cleaned_data['mood']
            emotion = get_emotion_max(mood)
            if emotion:
                if request.user.is_authenticated and emotion:
                    mood_instance = MoodInstance(
                        user=request.user, mood=mood, theme=emotion)
                    mood_instance.save()
        return redirect('virtual_agora_app:quote_from_mood', mood=mood)
    else:
        form = SubmitMoodForm()
    return render(request, 'index.html', {'form': form})


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
        obj = form.save(commit=False)
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


class PhilosopherQuoteListView(DetailView, MultipleObjectMixin):
    model = Philosopher
    template_name = 'philosopher_quote_list.html'
    context_object_name = 'philosopher'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        object_list = Quote.objects.filter(author=self.object).order_by('?')
        context = super(PhilosopherQuoteListView, self).get_context_data(
            object_list=object_list, **kwargs)
        return context


class QuoteListView(ListView):
    model = Quote
    template_name = 'quote_list.html'
    context_object_name = 'quotes'

    def get_queryset(self):
        return Quote.objects.order_by('?')

    paginate_by = 10


class QuoteCreateView(CreateView):
    model = Quote
    template_name = 'quote_create.html'
    form_class = QuoteCreateForm

    def change_theme(self, instance):
        instance.theme.add(Theme.objects.get(name="Happy"))
        print(instance.author)
        print(instance.theme.all())

    def form_valid(self, form):
        instance = form.save(commit=False)
        form.cleaned_data['theme'] = get_emotion_list(
            form.cleaned_data['title'])
        instance.save()
        return super().form_valid(form)


class QuoteDetailView(FormMixin, DetailView):
    model = Quote
    template_name = 'quote_detail.html'
    context_object_name = 'quote'
    form_class = CommentCreateForm

    def get_success_url(self):
        return reverse('virtual_agora_app:quote_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(QuoteDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentCreateForm(initial={'quote': self.object})
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
        obj = form.save(commit=False)
        obj.quote = self.object
        obj.save()
        return super(QuoteDetailView, self).form_valid(form)


class ThemeQuotesView(DetailView, MultipleObjectMixin):
    model = Theme
    template_name = 'quote_theme.html'
    context_object_name = 'theme'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        object_list = Quote.objects.filter(theme=self.object)
        context = super(ThemeQuotesView, self).get_context_data(
            object_list=object_list, **kwargs)
        return context


def GetQuoteFromMoodView(request, mood):
    emotion = get_emotion_max(mood)
    if emotion:
        quotes = Quote.objects.filter(theme__name=emotion).order_by('?')[:1]
        return render(request, 'quote_from_mood.html', {'quote': quotes.first(), 'mood': mood.title()})
    else:
        return render(request, 'quote_from_mood.html', {'quote': None, 'mood': mood.title()})


class ProfileView(TemplateView):
    template_name = 'profile.html'
