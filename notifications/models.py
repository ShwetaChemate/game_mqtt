from django.db import models
from django.contrib.auth.models import User

class GameEvent(models.Model):
    EVENT_CHOICES = [
        ('start', 'Game Started'),
        ('end', 'Game Ended'),
        ('pause', 'Game Paused'),
        ('resume', 'Game Resumed'),
        ('score', 'Score Update'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"prosumio {self.user.username} {self.message}"