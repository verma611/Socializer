from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


app_name= 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('Licence/', views.Licence, name='Licence'),
    path('/userslogout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

]
