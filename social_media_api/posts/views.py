from django.shortcuts import render
from .models import Post, Comment, Like
from rest_framework.exceptions import PermissionDenied
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, status, permissions
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType



# Create your views here.

class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    content = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['title', 'content']

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = PostPagination 
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = PostPagination
    

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user

    if Like.objects.filter(user=user, post=post).exists():
        return Response({'detail': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
    
    Like.objects.create(user=user, post=post)

    post_content_type = ContentType.objects.get_for_model(Post)
    Notification.objects.create(recipient=post.author,actor=user,verb='liked',target_content=post_content_type, target_object_id=post.id,target=post)
    return Response({'detail': 'Post liked successfully'}, status=status.HTTP_201_CREATED)

    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    like = Like.objects.filter(user=user, post=post).first()
    if not like:
        return Response({"detail": "You have not liked this post yet"}, status=status.HTTP_400_BAD_REQUEST)
    like.delete()
    return Response({"detail": "Post unliked successfully"}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    content = request.data.get("content")

    comment = Comment.objects.create(post=post, author=user, content=content)

    Notification.objects.create(recipient=post.author, actor=user, verb='commented on your post', target_content_type=ContentType.objects.get_for_model(Post),target_object_id=post.id, target=post)
    return Response({"detail": "Comment added successfully"}, status=status.HTTP_201_CREATED)
    

