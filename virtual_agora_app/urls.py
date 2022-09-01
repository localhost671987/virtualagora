from django.urls import path
from . import views

app_name = "virtual_agora_app"
urlpatterns = [
    path('', views.index, name='index'),
    path('post_list/', views.PostView.as_view(), name='post_list'),
]