from django.urls import path
from .views import EventListCreateView, EventDetailView, RSVPView

urlpatterns = [
    path(
      "api/events/",
      EventListCreateView.as_view(), name="event-list-create",
    ),
    path(
      "api/events/<int:pk>/",
      EventDetailView.as_view(),
      name="event-detail",
    ),
    path(
      "api/events/<int:pk>/rsvp/",
      RSVPView.as_view(),
      name="event-rsvp",
    ),
]
