import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from register.models import CustomUser
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']
        self.conversation_name = '_'.join(sorted([self.user.username, self.other_username]))
        self.room_group_name = f'chat_{self.conversation_name}'

        # Add to the WebSocket group
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

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Save message to the database
        await self.save_message(self.user, message)

        # Broadcast message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': self.user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        author = event['author']

        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
        }))

    @sync_to_async
    def save_message(self, user, message_text):
        # Perform the database operation in a synchronous-safe manner
        conversation, created = Conversation.objects.get_or_create(conversation_name=self.conversation_name)
        Message.objects.create(
            conversation=conversation,
            author=user,
            message=message_text
        )
