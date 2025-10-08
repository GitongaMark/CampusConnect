from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Conversation, DirectMessage


class UserPublicSerializer(serializers.ModelSerializer):
    """tiny version of user info — no private details"""

    class Meta:
        model = User
        fields = ["id", "username"]


class DirectMessageSerializer(serializers.ModelSerializer):
    sender_info = UserPublicSerializer(source="sender", read_only=True)

    class Meta:
        model = DirectMessage
        fields = [
          "id",
          "conversation",
          "sender",
          "sender_info",
          "content",
          "timestamp",
          "is_read",
          "read_at",
        ]
        read_only_fields = ["sender", "conversation", "timestamp", "read_at"]

    def update(self, instance, validated_data):
        """
        allow updating read status only (ie. marking message as read)
        """
        is_read = validated_data.get("is_read", None)
        if is_read and not instance.is_read:
            instance.is_read = True
            instance.read_at = timezone.now()
            instance.save()
        return instance


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserPublicSerializer(many=True, read_only=True)
    partner_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Conversation
        fields = [
          "id",
          "participants",
          "created_at",
          "partner_id"
        ]
        read_only_fields = ["participants", "created_at"]

    def validate_partner_id(self, value):
        user = self.context["request"].user
        if value == user.id:
            raise serializers.ValidationError("You can’t message yourself 😅")

        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("That user doesn’t exist.")
        return value

    def create(self, validated_data):
        #either get existing 1-on-1 chat or make a new one
        user = self.context["request"].user
        partner_id = validated_data.pop("partner_id", None)

        if not partner_id:
            raise serializers.ValidationError("Needs a partner_id to start a chat.")

        partner = User.objects.get(id=partner_id)

        # check if a chat between them already exists
        existing = (
            Conversation.objects.filter(participants=user)
            .filter(participants=partner)
            .first()
        )

        if existing:
            return existing

        # create a new one if none found
        convo = Conversation.objects.create(**validated_data)
        convo.participants.add(user, partner)
        return convo
