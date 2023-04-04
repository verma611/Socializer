from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('',  views.HomePage, name="HomePage"),
    path('posts', views.ShowAllPosts, name="ShowAllPosts"),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('new-post/', views.new_post, name='new_post'),
    path('like_post/<int:pk>', views.like_post, name="like_post"),
    path('dislike_post/<int:pk>', views.dislike_post, name="dislike_post"),
    path('search_posts', views.search_posts, name="search_posts"),
    path('my_posts', views.my_posts, name="my_posts"),
    path('delete_post/<int:pk>/', views.delete_a_post, name="delete_a_post"),
    path('edit_post/<int:pk>/', views.edit_post, name="edit_post"),
    path('settings/', views.user_profile_settings, name="user_profile_settings"),
    path('user_profile_settings/<int:pk>/', views.view_user_profile, name="view_user_profile"),
]
