from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


app_name = "virtual_agora_app"
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostView.as_view(), name='post_list'),
    path('my_posts/', views.MyPostsView.as_view(), name='my_posts'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post_detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post_delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('philosophers/', views.PhilosopherListView.as_view(), name='philosopher_list'),
    path('philosopher/<int:pk>', views.PhilosopherDetailView.as_view(), name='philosopher_detail'),
    path('philosopher/<int:pk>/quotes', views.PhilosopherQuoteListView.as_view(), name='philosopher_quotes'),
    path('quotes/', views.QuoteListView.as_view(), name='quote_list'),
    path('quote/<int:pk>', views.QuoteDetailView.as_view(), name='quote_detail'),
    path('quote_create/', views.QuoteCreateView.as_view(), name='quote_create'),
    path('quote_theme/<int:pk>/', views.ThemeQuotesView.as_view(), name='quote_theme'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
