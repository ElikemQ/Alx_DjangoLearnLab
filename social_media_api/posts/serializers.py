from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model
from .models import CustomUser


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    created_at = serializers.DateField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']

    def validate_title(self, value):
        if not value or len(value.strip()) <5:
            raise serializers.ValidationError('Post should be at least 10 characters long.')
        return value
    


class CommentSerializer(serializers.ModelSerializer):
        author = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
        post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
        created_at = serializers.DateTimeField(read_only=True)
        updated_at = serializers.DateTimeField(read_only=True)

        class Meta:
            model = Comment
            fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']

        def validate_content(self, value):
            if not value or len(value.strip()) < 5:
                raise serializers.ValidationError('Comment mut be at least 5 characters')
            return value 