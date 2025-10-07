from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import WalkRequest, WalkBuddy
from .serializers import WalkRequestSerializer, WalkBuddySerializer

class IsRequesterOrBuddy(IsAuthenticated):
  def has_object_permission(self, request, view, obj):
    user = request.user
    is_requester = obj.requester == user

    is_buddy = False
    try:
      if obj.match and obj.match.buddy == user:
        is_buddy = True
      
    except WalkBuddy.DoesNotExist:
      pass

    return is_requester or is_buddy

class WalkRequestListCreateView(generics.ListCreateAPIView):
  serializer_class = WalkRequestSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return WalkRequest.objects.filter(
      status__in=['PENDING', 'MATCHED']
    ).order_by('required_time')
  
  def perform_create(self, serializer):
    serializer.save(requester=self.request.user)

class WalkRequestAcceptView(generics.UpdateAPIView):
  queryset = WalkRequest.objects.all()
  serializer_class = WalkRequestSerializer
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kwargs):
    walk_request = self.get_object()
    
    #checks if user is accepting their own request
    if walk_request.requester == requst.user:
      return Response(
        {'detail': f'You cannot accept your own walk request.'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    #Is request still pending?
    if walk_request.status != 'PENDING':
      return Response(
        {'detail': 'Request is no longer available.'},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    #creating the walkbuddy object
    walk_match = WalkBuddy.objects.create(
      request=walk_request,
      partner=request.user
    )

    #updating the walk request to matched
    walk_request.status = 'MATCHED'
    walk_request.save()

    #return the updated request
    return Response(self.get_serializer(walk_request).data, status=status.HTTP_200_OK)

class WalkRequestDetailView(generics.RetrieveDestroyAPIView):
  queryset = WalkRequest.objects.all()
  serializer_class = WalkRequestSerializer
  permission_classes = [IsRequesterOrBuddy]

  def perform_destroy(self, instance):
    if instance.status in ['PENDING', 'MATCHED']:
      instance.status = 'CANCELLED'
      instance.save()
      return Response({'detail': 'Walk request successfully cancelled.'}, status=status.HTTP_200_OK)
    
    return super().perform_destroy(instance)

class WalkRequestCompleteView(generics.UpdateAPIView):
  queryset = WalkRequest.objects.all()
  serializer_class = WalkRequestSerializer
  permission_classes = [IsRequesterOrBuddy]

  def post(self, request, *args, **kwargs):
    walk_request = self.get_object()

    if walk_request.status != 'MATCHED':
      return Response(
        {'detail': f"Request status must be MATCHED to be completed. Current status: {walk_request.status}."},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    walk_request.status = 'COMPLETED'
    walk_request.save()

    return Response(self.get_serializer(walk_request).data, status=status.HTTP_200_OK)