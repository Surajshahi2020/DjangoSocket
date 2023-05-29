from channels.generic.websocket import AsyncWebsocketConsumer
import json, os, django
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from app.models import Room, ChatUser, Message


@sync_to_async
def create_room(room, username):
    user = ChatUser(name=username)
    user.save()
    room: Room = Room(name=room)
    room.save()
    room.username.add(user)
    print("data inserted into database")


@sync_to_async
def create_message(message, creator, room):
    chatuser = ChatUser.objects.get(name=creator)
    room = Room.objects.get(name=room)
    message = Message(creator=chatuser, content=message, room=room)
    message.save()
    print("message sent")


class MySocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data="Connected to the server")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        room = data.get("room")
        username = data.get("username")
        if room and username:
            await self.send(text_data="Message received by the server:" + text_data)
            await create_room(room, username)
        else:
            room = data.get("room")
            message = data.get("message")
            creator = data.get("creator")
            if message:
                await self.send(text_data="Message received by the server: " + message)
                await create_message(message, creator, room)
