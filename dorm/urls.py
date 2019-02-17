from django.urls import path
from . import views

app_name = 'dorm'
urlpatterns = [
    path('login/', views.LoginView, name='login'),
    path('register/', views.RegisterView, name='register'),
]

