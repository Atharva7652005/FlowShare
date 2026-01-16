from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    # Auth Urls
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_streamify, name="logout"),

    # Dashboard Urls
    path('dashboard/', views.dashboard, name='dashboard'),

    # Meeting Urls
    path('meeting/',views.videocall, name="new_meeting"),
    path('join/', views.join_meeting, name="join_meeting"),

    # File Urls
    path('drop_file/', views.drop_file, name="drop_file"),
    path('get_file/', views.get_file, name="get_file")
]
