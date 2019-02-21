from django.urls import path
from . import views

app_name = 'dormadmin'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.LogoutView, name='logout'),
    path('building/', views.BuildingView.as_view(), name='building'),
    path('building/<int:building_num>/', views.RoomView.as_view(), name='room'),
    path('building/<int:building_num>/<int:room_num>/', views.StudentView.as_view(), name='student'),
    path('search/', views.SearchView.as_view(), name='search'),
]
