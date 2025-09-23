from rest_framework import serializers # type: ignore
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
      
class ProfileSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
    model = Profile
    fields = ['id', 'user', 'major', 'email']

class RegisterSerializer(serializers.ModelSerializer):
  major = serializers.CharField(required=True)
  campus_email = serializers.EmailField(required=True)

  class Meta:
    model = User
    fields = ['username', 'email', 'password', 'major', 'campus_email']
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    major = validated_data.pop('major')
    campus_email = validated_data.pop('campus_email')
    user = User.objects.create_user(**validated_data)
    Profile.objects.create(user=user, major=major, campus_email=campus_email)
    return user
