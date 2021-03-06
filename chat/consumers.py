# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(WebsocketConsumer):

    # Connect and disconnect methods
    def connect(self):

        # FIXME: Anonymous user allowed to connect for testing. Got to remove second conditional

        if (self.scope["user"] != AnonymousUser() or self.scope["user"] == AnonymousUser()):
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close(code=1000)

    def disconnect(self, close_code):

        if (self.scope["user"] != AnonymousUser()):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        else:
            pass


# Receive method

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


# Receive message from front, save it DB and broadcast it to all channels

    def send_chat_message(self, data):

        message = Message(
            content=data['message'], sender=data['sender'], chatgroup=data['chatgroup'])
        message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': data
            }
        )

    def chat_message(self, data):
        message = data['data']['message']
        sender = data['data']['sender']
        self.send(text_data=json.dumps(
            [
                {
                    'message': message,
                    'sender': sender
                },
            ]
        )
        )


# Fetch messages for preload in front
    # Messages serializer

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'message': message.content,
            'sender': message.sender,
            'chatgroup': message.chatgroup,
            'timestamp': str(message.timestamp)
        }

    # Fetch messages functions
    def fetch_messages(self, data):
        chatgroup = data['chatgroup']
        messages = Message.objects.order_by(
            'timestamp').filter(chatgroup=chatgroup)

        self.send_message(self.messages_to_json(messages))

    def send_message(self, message):
        self.send(text_data=json.dumps(message))


# Commands dictionary
    commands = {
        'fetch_messages': fetch_messages,
        'send_chat_message': send_chat_message
    }
