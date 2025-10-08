from django.urls import path
from .views import (
    ConversationListCreateView,
    DirectMessageListCreateView,
    MarkMessageReadView,
)

# endpoints here — just chats and messages
urlpatterns = [
    path(
      "conversations/",
      ConversationListCreateView.as_view(), name="conversations",
    ),
    path(
        "conversations/<int:pk>/messages/",
        DirectMessageListCreateView.as_view(),
        name="messages",
    ),
    path(
        "messages/<int:pk>/read/",
        MarkMessageReadView.as_view(),
        name="mark-message-read",
    ),
]
