from django.db import models
from django.contrib.auth.models import User

class WalkRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Match'),
        ('MATCHED', 'Matched with Buddy'),
        ('COMPLETED', 'Walk Completed'),
        ('CANCELLED', 'Request Cancelled'),
    ]

    requester = models.ForeignKey(User, related_name='walk_requests', on_delete=models.CASCADE)
    start_location = models.CharField(max_length=200)
    end_location = models.CharField(max_length=200)
    required_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return f'WalkRequest by {self.requester.username} from {self.start_location} to {self.end_location} at {self.requested_time} ({self.status})'

class WalkBuddy(models.Model):
  request = models.OneToOneField(WalkRequest, on_delete=models.CASCADE, primary_key=True)
  buddy = models.ForeignKey(User, related_name='walk_buddies', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  matched_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Walkbuddy for {self.request.pk} with {self.buddy.username}'