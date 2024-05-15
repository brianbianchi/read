from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('user/<name>/', views.user, name='user'),
    path('feed/<int:id>/', views.view_feed, name='view_feed'),
    path('feeds', views.feeds, name='feeds'),
    path('create_feed/', views.create_feed, name='create_feed'),
    path('edit_feed/<int:id>/', views.edit_feed, name='edit_feed'),
]
