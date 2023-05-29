from django.urls import path
from .views import index, chatroom

urlpatterns = [
    path("lobby/", index, name="index"),
    path("lobby/<str:roomname>/", chatroom, name="chat"),
]
