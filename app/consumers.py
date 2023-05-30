from channels.generic.websocket import AsyncWebsocketConsumer
import json, os, django
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from app.models import Message
from channels.db import database_sync_to_async
from datetime import datetime


@sync_to_async
def create_message(message, creator, room):
    message = Message(room=room, content=message, creator=creator)
    message.save()
    return message


def getAllMessages(room):
    return Message.objects.filter(room=room).values(
        "content", "room", "creator", "created_at"
    )


class MySocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        params = self.scope["query_string"]
        scopes = params.decode("utf-8").split("&")
        room = scopes[0].split("=")[1]

        if room:
            messages = await sync_to_async(getAllMessages, thread_sensitive=True)(room)
            await self.accept()
            async for i in messages:
                created_at = i.get("created_at")
                created_at = datetime.strftime(created_at, "%Y-%m-%d %H:%M:%S")
                message_data = {
                    "room": i.get("room"),
                    "creator": i.get("content"),
                    "created_at": created_at,
                }
                await self.send(text_data=json.dumps(message_data))
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        room = data.get("room")
        creator = data.get("creator")
        message = data.get("message")
        if message:
            message = await create_message(message, creator, room)
            created_at = datetime.strftime(message.created_at, "%Y-%m-%d %H:%M:%S")
            message_data = {
                "room": message.room,
                "creator": message.creator,
                "created_at": created_at,
                "content": message.content,
            }
            await self.send(text_data=json.dumps(message_data))
