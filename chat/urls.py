from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
        path('friends', views.friend_list, name='friend_list'),
        path('chat_history/<int:friend_id>', views.chat_history, name='chat_history'),
        path('send_message/<int:friend_id>', views.send_message, name='send_message')
]
