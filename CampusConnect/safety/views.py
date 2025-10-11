from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.shortcuts import get_object_or_404
from .models import WalkRequest, WalkBuddy, WalkFeedback
from .serializers import WalkRequestSerializer, WalkFeedbackSerializer


class IsRequesterOrBuddy(BasePermission):
    """Allow access to the requester or their matched buddy."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_requester = obj.requester == user
        is_buddy = hasattr(obj, "match") and obj.match.buddy == user
        return is_requester or is_buddy


class WalkRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = WalkRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Show only active requests (pending or matched)."""
        return WalkRequest.objects.filter(status__in=["PENDING", "MATCHED"]).order_by("required_time")

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class WalkRequestAcceptView(APIView):
    """Allow a user to accept someone else's pending walk request."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        walk_request = get_object_or_404(WalkRequest, pk=pk)

        if walk_request.requester == request.user:
            return Response(
                {"detail": "You cannot accept your own walk request."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if walk_request.status != "PENDING":
            return Response(
                {"detail": "Request is no longer available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        WalkBuddy.objects.create(request=walk_request, buddy=request.user)
        walk_request.status = "MATCHED"
        walk_request.save()

        serializer = WalkRequestSerializer(walk_request, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class WalkRequestDetailView(generics.RetrieveDestroyAPIView):
    queryset = WalkRequest.objects.all()
    serializer_class = WalkRequestSerializer
    permission_classes = [IsRequesterOrBuddy]

    def perform_destroy(self, instance):
        """Cancel a pending or matched request."""
        if instance.status in ["PENDING", "MATCHED"]:
            instance.status = "CANCELLED"
            instance.save()
            return Response({"detail": "Walk request cancelled."}, status=status.HTTP_200_OK)
        return super().perform_destroy(instance)


class WalkRequestCompleteView(APIView):
    """Mark a walk as completed (by requester or buddy)."""

    permission_classes = [IsRequesterOrBuddy]

    def post(self, request, pk):
        walk_request = get_object_or_404(WalkRequest, pk=pk)

        if walk_request.status != "MATCHED":
            return Response(
                {"detail": f"Request must be MATCHED before marking complete (current: {walk_request.status})."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        walk_request.status = "COMPLETED"
        walk_request.save()

        serializer = WalkRequestSerializer(walk_request, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class WalkFeedbackCreateView(generics.CreateAPIView):
    """Allows a requester or buddy to leave feedback after a completed walk."""

    serializer_class = WalkFeedbackSerializer
    permission_classes = [IsRequesterOrBuddy]

    def perform_create(self, serializer):
        walk_request = get_object_or_404(WalkRequest, pk=self.kwargs["pk"])

        if walk_request.status != "COMPLETED":
            raise serializers.ValidationError("Feedback can only be left after the walk is completed.")

        user = self.request.user
        if not hasattr(walk_request, "match"):
            raise serializers.ValidationError("This walk has no assigned buddy.")

        # Determine who is being reviewed
        if walk_request.requester == user:
            reviewed_user = walk_request.match.buddy
        elif walk_request.match.buddy == user:
            reviewed_user = walk_request.requester
        else:
            raise serializers.ValidationError("You are not part of this walk request.")

        serializer.save(
            walk_request=walk_request,
            reviewer=user,
            reviewed_user=reviewed_user,
        )
