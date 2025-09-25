from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10,
    choices=[('going', 'Going'), ('maybe', 'Maybe'), ('not going', 'Not Going')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

        class Meta:
          unique_together = ('event', 'user')

        def __str__(self):
          return f'{self.user.username} RSVP for {self.event.title} as {self.status}'