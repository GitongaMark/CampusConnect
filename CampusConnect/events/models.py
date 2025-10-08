from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    # basic event info
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} on {self.date}"


class RSVP(models.Model):
    STATUS_CHOICES = [
        ("going", "Going"),
        ("maybe", "Maybe"),
        ("not going", "Not Going"),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rsvps")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user.username} RSVP’d for '{self.event.title}' as {self.status}"
