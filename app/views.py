from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def chatroom(request, roomname):
    return render(request, "chat.html")
