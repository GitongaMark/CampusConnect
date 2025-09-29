from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, StudyGroup, Message, Meeting

class CourseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Course
    fields = ['id', 'name', 'code']
  
class UserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ['id', 'username']
    
class MessageSerializer(serializers.ModelSerializer):
   username = serializers.CharField(source='user.username', read_only=True)

   class Meta:
      model = Message
      fields = ['id', 'group', 'user', 'username','content', 'timestamp']
      read_only_fields = ['user', 'group']

class MeetingSerializer(serializers.ModelSerializer):
   created_by_username = serializers.CharField(source='created_by.username', read_only=True)

   class Meta:
      model = Meeting
      fields = ['id', 'group', 'title', 'agenda', 'location', 'scheduled_time', 'created_by', 'created_by_username', 'created_at']
      read_only_fields = ['created_by', 'group']

class StudyGroupSerializer(serializers.ModelSerializer):
   course_code = serializers.CharField(source='course.code', read_only=True)
   members = UserSerializer(many=True, read_only=True)
   member_count = serializers.SerializerMethodField()
   meetings = MeetingSerializer(many=True, read_only=True)

   class Meta:
      model = StudyGroup
      fields = ['id', 'name', 'course', 'course_code', 'members', 'member_count', 'meetings']
      read_only_fields = ['members']

   def get_member_count(self, obj):
       return obj.members.count()