from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
import json
from . import models
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['name']

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        await self.fetch_history()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        time = await self.create_messages(message=text_data_json['message'], sender_id=text_data_json['sender_id'])
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': text_data_json['message'],
                'sender_id': text_data_json['sender_id'],
                'time': time
            }
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                'message': event['message'],
                'sender_id': event['sender_id'],
                'time': event['time']
            })
        )

    @database_sync_to_async
    def create_messages(self, message, sender_id):
        chatgroup = models.ChatGroup.objects.get(name=self.room_name)
        sender = models.User.objects.get(id=sender_id)
        message = models.Message.objects.create(
            body=message,
            sender=sender,
            chatgroup=chatgroup
        )
        return message.time.strftime('%d-%h %H:%M')

    async def fetch_history(self):
        messages = await self.history_messages()
        for message in messages:
            await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def history_messages(self):
        chatgroup = models.ChatGroup.objects.get(name=self.room_name)
        messages = models.Message.objects.filter(chatgroup=chatgroup)
        serialized_messages = [
            {
                'message': message.body,
                'sender_id': message.sender.id,
                'time': message.time.strftime('%d-%h %H:%M')
            }
            for message in messages
        ]
        return serialized_messages


class ProfileListConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user_id = self.scope['user'].id
        self.group_name = "online_users"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.change_status("online")
        await self.channel_layer.group_send(self.group_name, {'type': 'user_list'})

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.change_status(datetime.now().strftime('%d-%h %H:%M'))
        await self.channel_layer.group_send(self.group_name, {'type': 'user_list'})

    async def receive(self):
        pass

    async def user_list(self, event):
        users = await self.all_users()
        await self.send(text_data=json.dumps(users))

    @database_sync_to_async
    def all_users(self):
        profiles = models.Profile.objects.all()
        serialized_profiles = [
            {
                'full_name': profile.user.get_full_name(),
                'username': profile.user.username,
                'status': profile.status,
                'picture': profile.image.url,
            } for profile in profiles
        ]
        return serialized_profiles

    async def change_status(self, status):
        await self.update_profile(status=status)

    @database_sync_to_async
    def update_profile(self, status):
        profile = models.Profile.objects.get(user_id=self.user_id)
        profile.status = status
        profile.save()
