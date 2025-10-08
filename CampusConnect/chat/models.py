from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Conversation(models.Model):
    # basic chat between two or more users
    participants = models.ManyToManyField(User, related_name="chats")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # just show usernames joined by commas
        names = [u.username for u in self.participants.all()]
        return f"Chat: {', '.join(names)}"


class DirectMessage(models.Model):
    # a single message inside a chat
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)  # whether recipient has seen it
    read_at = models.DateTimeField(null=True, blank=True)  # when it was read (if at all)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        # show sender, time, and short content preview
        return f"{self.sender.username} @ {self.timestamp:%H:%M} — {self.content[:30]}"

    # TODO: could later trigger notification when message marked as read
