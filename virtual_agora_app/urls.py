from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "virtual_agora_app"
urlpatterns = [
    path('', views.index, name='index'),
    path('post_list/', views.PostView.as_view(), name='post_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)