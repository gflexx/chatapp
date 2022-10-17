from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive msg from websocket
    async def receive(self, text_data):
        json_text = json.loads(text_data)
        msg = json_text['message']

        # send msg to group room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg
            }
        )

        
    async def chat_message(self, event):
        msg = event['message']

        # send msg to websocket
        await self.send(
            text_data=json.dumps({
                'message': msg,
            })
        )
