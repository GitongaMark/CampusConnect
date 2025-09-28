from django.urls import path
from .views import CourseListView, StudyGroupListCreateView, StudyGroupJoinView, MessageListCreateView, MeetingListCreateView

urlpatterns = [
  #Course endpoints
  path('api/courses/', CourseListView.as_View(), name='course-list'),
  path('api/courses/<int:course_id>/groups/', StudyGroupListCreateView.as_view(), name='course-group-list'),

  #Study Group Endpoints
  path('api/study_groups/', StudyGroupListCreateView.as_view(), name='study-group-create'),
  path('api/study_groups/<int:pk>/join/', StudyGroupJoinView.as_view, name='study-group-join'),

  #Messaging Endpoints
  path('api/study_groups/<int:group_id>/messages/', MessageListCreateView.as_view(), name='group-message-list-create'),

  #Meeting endpoints
  path('api/study_groups/<int:group_id>/meetings/', MeetingListCreateView.as_view(), name='group-meeting-list-create'),
]