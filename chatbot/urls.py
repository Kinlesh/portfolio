# chatbot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.WelcomeView.as_view(), name='welcome'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.LoginInterfaceView.as_view(), name='login'),
    path('chat/', views.ChatbotView.as_view(), name='chat'),
]
