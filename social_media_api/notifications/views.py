from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from notifications.models import Notification
from .models import CustomUser


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    try:
        target_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user == target_user:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    if user.following.filter(id=target_user.id).exists():
        return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

    user.following.add(target_user)

    Notification.objects.create(
        recipient=target_user,
        actor=user,
        verb='started following you',
        target_content_type=None,  
        target_object_id=None,
        target=None
    )
    return Response({"detail": "Successfully followed the user."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        target_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if not user.following.filter(id=target_user.id).exists():
        return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
    user.following.remove(target_user)
    return Response({"detail": "Successfully unfollowed the user."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')

    unread_notifications = notifications.filter(read=False)
    unread_notifications.update(read=True)

    notification_data = [
        {
            "id": notification.id, "actor": notification.actor.username, "verb": notification.verb, "timestamp": notification.timestamp, "target": str(notification.target) if notification.target else None, "read": notification.read }
        for notification in notifications
    ]
    return Response({"notifications": notification_data}, status=status.HTTP_200_OK)