from django.urls import path
from . import views

app_name = 'ingestion'

urlpatterns = [
    path('status/', views.ingestion_status, name='status'),
    path('posts/', views.posts_list, name='posts_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('logs/', views.ingestion_logs, name='logs'),
]
