from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Notification
from .serializer import NotificationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


# Create your views here.
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only notifications where the logged-in user is the recipient
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, pk):
    notif = Notification.objects.filter(pk=pk, recipient=request.user).first()
    if not notif:
        return Response({'detail': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)
    notif.read = True
    notif.save()
    return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    Notification.objects.filter(recipient=request.user, read=False).update(read=True)
    return Response({'detail': 'All notifications marked as read.'}, status=status.HTTP_200_OK)