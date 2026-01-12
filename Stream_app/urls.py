from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('meeting/',views.videocall, name="new_meeting"),
    path('join/', views.join_meeting, name="join_meeting"),
    path('logout/', views.logout_streamify, name="logout")
]
