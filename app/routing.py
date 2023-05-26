from django.urls import path
from app import consumers

websocket_urlpatterns = [
    path("ws/my_socket/", consumers.MySocketConsumer.as_asgi()),
]
