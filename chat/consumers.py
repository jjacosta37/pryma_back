# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    # Connect and disconnect methods

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
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


# Receive method and commands


    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


# Receive message from front, save it DB (TODO) and broadcast it to all channels


    def send_chat_message(self, data):
        print('send_chat_message')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': data
            }
        )

    # Receive message from room group
    def chat_message(self, data):
        print('chat_message')
        message = data['data']['message']
        print(message)
        self.send(text_data=json.dumps(
            [
                {
                    'message': message
                },
            ]
        )
        )


# TODO Fetch messages for preload in front


# Commands dictionary

    commands = {
        # 'fetch_messages': fetch_messages,
        'send_chat_message': send_chat_message
    }
