from channels.generic.websocket import AsyncWebsocketConsumer


class MySocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send("Connected to the server")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send("Message received by the server:" + text_data)
