from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from django.core import serializers
import json

from .models import Message

Users = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def get_messages(self, data):
        msgs = Message.get_last_10_msgs()
        content = {
            'messages': self.messages_to_json(msgs)
        }
        self.send_message(content)

    def new_message(self, data):
        owner = data['owner']
        user = Users.objects.filter(id=owner)[0]
        msg = Message.objects.create(
            owner=user,
            text=data['text']
        )
        content = {
            'message': self.serialize_msg(msg)
        }
        


    def messages_to_json(self, msgs):
        results = []
        for msg in msgs:
            results.append(self.serialize_msg(msg))
        return results

    def serialize_msg(self, msg):
        data = {
            'author': msg.owner.username,
            'text': msg.text,
            'created_at': str(msgs.created_at)
        }
        return data

    commands = {
        'get_messages': get_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # receive msg from websocket
    def receive(self, text_data):
        data = json.loads(text_data)
        msg = data['message']
        self.commands[data['command']](self, data)

    # send msg to group room
    def send_chat_message(self, msg):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg
            }
        )

    def send_message(self, msg):
        self.send(text_data=json.dumps(msg)) 

    def chat_message(self, event):
        msg = event['message']
        self.send(text_data=json.dumps(msg))
        