# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'chatgpt'
urlpatterns = [

    path('', views.index, name='index'),
    path('chat', views.chat_view, name='chat'),
    path('clear_chat', views.clear_chat, name='clear_chat'),
    path('sign', views.sign, name='sign'),
    
]
