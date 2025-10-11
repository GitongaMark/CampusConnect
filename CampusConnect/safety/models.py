from django.db import models
from django.contrib.auth.models import User


class WalkRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending Match"),
        ("MATCHED", "Matched with Buddy"),
        ("COMPLETED", "Walk Completed"),
        ("CANCELLED", "Request Cancelled"),
    ]

    requester = models.ForeignKey(User, related_name="walk_requests", on_delete=models.CASCADE)
    start_location = models.CharField(max_length=200)
    end_location = models.CharField(max_length=200)
    required_time = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"WalkRequest({self.requester.username}: "
            f"{self.start_location} → {self.end_location} at {self.required_time:%Y-%m-%d %H:%M} — {self.status})"
        )


class WalkBuddy(models.Model):
    """A user who accepts a walk request and becomes a walking buddy."""

    request = models.OneToOneField(WalkRequest, on_delete=models.CASCADE, related_name="match")
    buddy = models.ForeignKey(User, related_name="walk_buddies", on_delete=models.CASCADE)
    matched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Buddy({self.buddy.username} ↔ Request {self.request.id})"


class WalkFeedback(models.Model):
    """Feedback left by one user for another after a completed walk."""

    walk_request = models.ForeignKey(WalkRequest, on_delete=models.CASCADE, related_name="feedbacks")
    reviewer = models.ForeignKey(User, related_name="given_feedbacks", on_delete=models.CASCADE)
    reviewed_user = models.ForeignKey(User, related_name="received_feedbacks", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("walk_request", "reviewer")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reviewer.username} → {self.reviewed_user.username} ({self.rating}/5)"
