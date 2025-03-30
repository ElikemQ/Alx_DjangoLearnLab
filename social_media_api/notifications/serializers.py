from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from posts.serializers import PostSerializer
from posts.models import Post

class NotificationSerializer(serializers.ModelSerializer):
    recipient  = serializers.StringRelatedField()
    actor = serializers.StringRelatedField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['recipient', 'actor', 'verb', 'target', 'timestamp']

    def get_target(self, obj):
        target_serializer = None
        if isinstance(obj.target, Post):
            target_serializer = PostSerializer(obj.target)
        
        return target_serializer.data if target_serializer else None
    