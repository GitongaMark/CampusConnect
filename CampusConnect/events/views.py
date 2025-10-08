from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Event, RSVP
from .serializers import EventSerializer, RSVPSerializer


class EventListCreateView(generics.ListCreateAPIView):
    """List all events or create a new one"""
    queryset = Event.objects.all().order_by("-date")
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # save event with current user as creator
        serializer.save(created_by=self.request.user)


class EventDetailView(generics.RetrieveAPIView):
    """Retrieve details of a specific event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class RSVPView(APIView):
    """Handle RSVP creation and updates"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        status_choice = request.data.get("status", "going")
        if status_choice not in dict(RSVP.STATUS_CHOICES):
            return Response({"error": "Invalid RSVP status"}, status=status.HTTP_400_BAD_REQUEST)

        rsvp, created = RSVP.objects.update_or_create(
            event=event, user=request.user, defaults={"status": status_choice}
        )

        serializer = RSVPSerializer(rsvp)
        return Response(
            {"message": "RSVP updated" if not created else "RSVP created", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
