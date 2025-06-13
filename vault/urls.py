from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_password, name='add'),
    path('delete/<int:id>/', views.delete_password, name='delete'),
    path('login/', auth_views.LoginView.as_view(template_name='vault/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
]
