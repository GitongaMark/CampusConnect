from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
  participants = models.ManyToManyField(User, related_name='conversations')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    usernames = ', '.join(self.participants.values_list('username', flat=True))
    return f'Conversation between {usernames}'

class DirectMessage(models.Model):
  conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)

  sender = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['timestamp']

  def __str__(self):
    return f'Message from {self.sender.username}'