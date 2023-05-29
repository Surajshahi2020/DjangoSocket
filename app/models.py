from django.db import models


class ChatUser(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"


class Room(models.Model):
    name = models.CharField(max_length=255)
    username = models.ManyToManyField(ChatUser)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    creator = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.creator} -- in -- {self.room}"
