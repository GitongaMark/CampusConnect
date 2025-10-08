from rest_framework import serializers
from .models import Event, RSVP


class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Event
        fields = [
          "id",
          "title",
          "description",
          "date",
          "time",
          "location",
          "created_by",
          "created_at",
        ]


class RSVPSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    event_title = serializers.ReadOnlyField(source="event.title")

    class Meta:
        model = RSVP
        fields = [
          "id",
          "event",
          "event_title",
          "user",
          "status",
          "timestamp"
        ]
        read_only_fields = ["user", "timestamp"]
