from django.shortcuts import render
from django.contrib.auth.models import update_last_login
from rest_framework import generics, status
from rest_framework. views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, CustomUserSerializer
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser

# Create your views here.

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                update_last_login(None, user)
                return Response({'token': token.key, 'user': CustomUserSerializer(user).data})
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

class FollowUnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        user = request.user

        if user == user_to_follow:
            return Response({'detail': "You can't follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.following.add(user_to_follow)
        return Response({'detail': f"You're now following {user_to_follow.username}."}, status=status.HTTP_200_OK)
    
    def delete(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        user = request.user

        if user == user_to_unfollow:
            return Response({'detail': "You can't unfollow yourself,."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.following.remove(user_to_unfollow)
        return Response({'detail': f"You've unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
    