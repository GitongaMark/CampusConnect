from rest_framework import serializers
from .models import WalkRequest, WalkBuddy
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username']

class WalkBuddySerializer(serializers.ModelSerializer):
  buddy_details = UserSerializer(source='buddy', read_only=True)

  class Meta:
    model = WalkBuddy
    fields = ['id', 'buddy', 'buddy_details', 'matched_at']
    read_only_fields = ['buddy', 'matched_at']

class WalkRequestSerializer(serializers.ModelSerializer):
  requester_details = UserSerializer(source='requester', read_only=True)
  match = WalkBuddySerializer(read_only=True)

  class Meta:
    model = WalkRequest
    fields = ['id', 'requester', 'requester_details', 'start_location', 'end_location', 'required_time', 'status', 'created_at', 'match']
    read_only_fields = ['requester', 'status']

