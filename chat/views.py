from django.http import request
from django.shortcuts import render

def profile(request):
    template_name = 'profile.html'
    context = {
        'title': 'Profile',
    }
    return render(request, template_name, context)

def chat_room(request, room_name): 
    template_name = 'chat_room.html'
    context = {
        'title': 'Chat Room',
        'room_name': room_name,
    }
    return render(request, template_name, context)

