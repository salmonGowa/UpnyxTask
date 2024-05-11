# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.login_user, name='login'),
    path('api/chat/', views.chat, name='chat'),
    path('api/token-balance/', views.token_balance, name='token_balance'),
]
