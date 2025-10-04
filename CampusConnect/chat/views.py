from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Conversation, DirectMessage
from .serializers import ConversationSerializer, DirectMessageSerializer

class ConversationListCreateView(generics.ListCreateAPIView):
  serializer_class = ConversationSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return Conversation.objects.filter(participants=self.request.user).order_by('created_at')
  
  def get_serializer_context(self):
    return {'request': self.request}

class DirectMessageListCreateView(generics.ListCreateAPIView):
  serializer_class = DirectMessageSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    conversation_id = self.kwargs['pk']
    conversation = get_object_or_404(
      Conversation.objects.filter(participants=self.request.user),
      pk=conversation_id
    )

    return DirectMessage.objects.filter(conversation=conversation)

  def perform_create(self, serializer):
    conversation_id = self.kwargs['pk']
    user = self.request.user

    conversation = get_object_or_404(
      Conversation.objects.filter(participants=user),
      pk=conversation_id
    )

    serializer.save(conversation=conversation, sender=user)