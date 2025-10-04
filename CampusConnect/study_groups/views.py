from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Course, StudyGroup, Message, Meeting
from .serializers import CourseSerializer, StudyGroupSerializer, MessageSerializer, MeetingSerializer

class CourseListView(generics.ListAPIView):
  queryset = Course.objects.all()
  serializer_class = CourseSerializer
  permission_classes = [IsAuthenticated]

class StudyGroupListCreateView(generics.ListCreateAPIView):
  serializer_class = StudyGroupSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    course_id = self.kwargs.get('course_id')
    if course_id:
      course = get_object_or_404(Course, pk=course_id)
      return StudyGroup.objects.filter(course=course)
    return StudyGroup.objects.all()
  
  def perform_create(self, serializer):
    group = serializer.save()
    group.members.add(self.request.user)

class StudyGroupJoinView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request,pk):
    study_group = get_object_or_404(StudyGroup, pk=pk)
    study_group.members.add(request.user)

    return Response({'status': f'Successfully joined {study_group.name}'}, status=status.HTTP_200_OK)

class MessageListCreateView(generics.ListCreateAPIView):
  serializer_class = MessageSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    group_id = self.kwargs['group_id']
    study_group = get_object_or_404(StudyGroup, pk=group_id)

    if not study_group.members.filter(id=self.request.user.id).exists():
      return Message.objects.none()
    return Message.objects.filter(group=study_group)
  def perform_create(self, serializer):
    group_id = self.kwargs['group_id']
    study_group = get_object_or_404(StudyGroup, pk=group_id)

    if not study_group.members.filter(id=self.request.user.id).exists():
      raise serializers.ValidationError("You must be a member of the group to post messages.")
    
    serializer.save(group=study_group, user=self.request.user)

class MeetingListCreateView(generics.ListCreateAPIView):
  serializer_class = MeetingSerializer
  permission_classes = [IsAuthenticated]
  
  def get_queryset(self):
    group_id = self.kwargs['group_id']
    study_group = get_objects_or_404(StudyGroup, pk=group_id)

    if not study_group.members.filter(id=self.request.user.id).exists():
      return Meeting.objects.none()
    
    return Meeting.objects.filter(group=study_group)
  
  def perform_create(self, serializer):
    group_id = self.kwargs['group_id']
    study_group = get_object_or_404(StudyGroup, pk=group_id)

    if not study_group.members.filter(id=self.request.user.id).exists():
      raise serializers.ValidationError('You must be a member of the group to schedule a meeting.')

    serializer.save(group=study_group, created_by=self.request.user)