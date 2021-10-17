from django.urls import re_path

websocket_routes = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$)', ),
]