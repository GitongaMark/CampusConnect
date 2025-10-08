from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import Conversation, DirectMessage
from .serializers import ConversationSerializer, DirectMessageSerializer


class ConversationListCreateView(generics.ListCreateAPIView):
    """list all chats for the user, or start a new one"""

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by(
            "-created_at"
        )

    def get_serializer_context(self):
        return {"request": self.request}


class DirectMessageListCreateView(generics.ListCreateAPIView):
    """show or send messages within a conversation"""

    serializer_class = DirectMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        convo_id = self.kwargs["pk"]
        convo = get_object_or_404(
            Conversation.objects.filter(participants=self.request.user),
            pk=convo_id,
        )
        return convo.messages.all()

    def perform_create(self, serializer):
        convo_id = self.kwargs["pk"]
        user = self.request.user
        convo = get_object_or_404(
            Conversation.objects.filter(participants=user), pk=convo_id
        )
        serializer.save(conversation=convo, sender=user)


class MarkMessageReadView(generics.UpdateAPIView):
    """mark a message as read"""

    serializer_class = DirectMessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = DirectMessage.objects.all()

    def patch(self, request, *args, **kwargs):
        message = get_object_or_404(
            DirectMessage.objects.filter(conversation__participants=request.user),
            pk=kwargs["pk"],
        )

        if not message.is_read:
            message.is_read = True
            message.read_at = timezone.now()
            message.save()

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
