from django.urls import path
from .views import (
  WalkRequestListCreateView,
  WalkRequestAcceptView,
  WalkRequestDetailView,
  WalkRequestCompleteView,
  WalkFeedbackCreateView,
)

urlpatterns = [
  #List active requests and create new requests
  path('api/safety/requests/', WalkRequestListCreateView.as_view(), name='walk-request-list-create'),

  #Accepting a pending request
  path('api/safety/requests/<int:pk>/accept/', WalkRequestAcceptView.as_view(), name='walk-request-accept'),

  #Marks a walk as completed
  path('api/safety/requests/<int:pk>/complete/', WalkRequestCompleteView.as_view(), name='walk-request-complete'),

  #Retrieve or cancel request
  path('api/safety/requests/<int:pk>/', WalkRequestDetailView.as_view(), name='walk-request-detail'),

  #Leave a comment and rating for a completed walk
  path("api/safety/requests/<int:pk>/feedback/", WalkFeedbackCreateView.as_view(), name="walk-feedback-create"),
]