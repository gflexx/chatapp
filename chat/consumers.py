from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        json_text = json.loads(text_data)
        msg = json_text['message']

        self.send(
            text_data=json.dumps({
                'message': msg,
            })
        )