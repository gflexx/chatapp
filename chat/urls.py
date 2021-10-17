from django.urls import path, include

from .views import *

urlpatterns = [
    path('profile', profile, name='profile'),
    path('<str:room_name>', chat_room, name='chat_room'),
]