from rest_framework import serializers
from django.contrib.auth.models import User
from .models import WalkRequest, WalkBuddy, WalkFeedback


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class WalkBuddySerializer(serializers.ModelSerializer):
    buddy_details = UserSerializer(source="buddy", read_only=True)

    class Meta:
        model = WalkBuddy
        fields = ["id", "buddy", "buddy_details", "matched_at"]
        read_only_fields = ["buddy", "matched_at"]


class WalkFeedbackSerializer(serializers.ModelSerializer):
    reviewer_details = UserSerializer(source="reviewer", read_only=True)
    reviewed_user_details = UserSerializer(source="reviewed_user", read_only=True)

    class Meta:
        model = WalkFeedback
        fields = [
            "id",
            "walk_request",
            "reviewer",
            "reviewer_details",
            "reviewed_user",
            "reviewed_user_details",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["reviewer", "created_at", "walk_request", "reviewed_user"]


class WalkRequestSerializer(serializers.ModelSerializer):
    requester_details = UserSerializer(source="requester", read_only=True)
    match = WalkBuddySerializer(read_only=True)
    feedbacks = WalkFeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = WalkRequest
        fields = [
            "id",
            "requester",
            "requester_details",
            "start_location",
            "end_location",
            "required_time",
            "status",
            "created_at",
            "match",
            "feedbacks",
        ]
        read_only_fields = ["requester", "status", "created_at"]
