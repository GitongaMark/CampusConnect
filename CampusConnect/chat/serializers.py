from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, DirectMessage

class UserPublicSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username']

class DirectMessageSerializer(serializers.ModelSerializer):
  sender_details = UserPublicSerializer(source='sender', read_only=True)

  class Meta:
    model = DirectMessage
    fields = ['id', 'conversation', 'sender', 'sender_details', 'content', 'timestamp']
    read_only_fields = ['sender', 'conversation']

class ConversationSerializer(serializers.ModelSerializer):
  participants = UserPublicSerializer(many=True, read_only=True)
  partner_id = serializers.IntegerField(write_only=True, required=False)

  class Meta:
    model = Conversation
    fields = ['id', 'participants', 'created_at', 'partner_id']
    read_only_fields = ['participants']

  def validate_partner_id(self, value):
    if value == self.context['request'].user.id:
      raise serializers.ValidationError("You cannot start a conversation with yourself.")
    
    if not User.objects.filter(id=value).exists():
      raise serializer.ValidationError("The specified partner ID does not exists.")
    
    return value
  
  def create(self, validated_data):
    user = self.context['request'].user
    partner_id = validated_data.pop('partner_id', None)

    if not partner_id:
      raise serializers.ValidationError("Partner ID is required to start a conversation.")

      partner = User.objects.get(id=partner_id)

      existing_conversations = Conversation.objects.filter(
        participants=user
      ).filter(
        participants=partner
      ).annotate(
        num_participants=models.Count('participants')
      ).filter(
        num_participants=2
      )

      if existing_conversations.exists():
        return existing_conversations.first()
      
      conversation = Conversation.objects.create(**validated_data)
      conversation.participants.add(user, partner)
      return conversation