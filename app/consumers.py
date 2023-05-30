from channels.generic.websocket import AsyncWebsocketConsumer
import json, os, django
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from app.models import Room, ChatUser, Message
from channels.db import database_sync_to_async
from datetime import datetime


@sync_to_async
def create_room(room, username):
    user = ChatUser(name=username)
    user.save()
    room: Room = Room(name=room)
    room.save()
    room.username.add(user)


@sync_to_async
def create_message(message, creator, room):
    chatuser = ChatUser.objects.filter(name=creator).first()
    room = Room.objects.filter(name=room).first()
    message = Message(creator=chatuser, content=message, room=room)
    message.save()
    return message


def getAllMessages():
    return Message.objects.all().values("content", "room", "creator", "created_at")


class MySocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        messages = await sync_to_async(getAllMessages, thread_sensitive=True)()
        async for i in messages:
            room_id = i.get("room")
            creator_id = i.get("creator")
            created_at = i.get("created_at")
            room = await sync_to_async(Room.objects.get, thread_sensitive=True)(
                id=room_id
            )
            creator = await sync_to_async(ChatUser.objects.get, thread_sensitive=True)(
                id=creator_id
            )
            created_at = datetime.strftime(created_at, "%Y-%m-%d %H:%M:%S")
            message_data = {
                "room": room.name,
                "creator": creator.name,
                "created_at": created_at,
            }
            i.update(message_data)
            await self.send(text_data=json.dumps(i))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        room = data.get("room")
        username = data.get("username")
        if room and username:
            await create_room(room, username)
        else:
            room = data.get("room")
            creator = data.get("creator")
            message = data.get("message")
            if message:
                message = await create_message(message, creator, room)
                created_at = datetime.strftime(message.created_at, "%Y-%m-%d %H:%M:%S")

                message_data = {
                    "room": message.room.name,
                    "creator": message.creator.name,
                    "created_at": created_at,
                    "content": message.content,
                }
                await self.send(text_data=json.dumps(message_data))
