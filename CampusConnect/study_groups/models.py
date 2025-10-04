from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.code}: {self.name}"

class StudyGroup(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='study_groups')

    def __str__(self):
        return f'Group: {self.name} ({self.course.code})'
    
class Message(models.Model):
    group = models.ForeignKey(StudyGroup, related_name='message', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f'Message from {self.user.name} in {self.group.name} at {self.timestamp}'
  
class Meeting(models.Model):
    group = models.ForeignKey(StudyGroup, related_name='meetings', on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    agenda = models.TextField()
    location = models.CharField(max_length=200)
    scheduled_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_time']

    def __str__(self):
        return f'{self.title} for {self.group.name} on {self.scheduled_time.strftime("%Y-%m-%d")}'