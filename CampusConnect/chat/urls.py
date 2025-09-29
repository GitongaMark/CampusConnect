from django.urls import path
from .views import ConversationListCreateView, DirectMessageListCreateView

urlpatterns = [
  path('api/chat/conversations/', ConversationListCreateView.as_view(), name='conversation-list-create'),
  path('api/chat/conversations/<int:pk>/messages/', DirectMessageListCreateView.as_view(), name='direct-message-list-create')
]