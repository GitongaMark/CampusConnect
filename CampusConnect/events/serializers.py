from rest_framework import serializers
from .models import Event, RSVP

class EventSerializer(serializers.ReadOnlyField):
  created_by = serializers.ReadOnlyField(source='created_by.username')

  class Meta:
    model = Event
    fields = ['id', 'title', 'description', 'date', 'time', 'location', 'created_by']

class RSVPSerializer(serializers.ModelSerializer):
  class Meta:
    model = RSVP
    fields = ['id', 'event', 'user', 'status', 'timestamp']
    read_only_fields = ['user', 'timestamp']