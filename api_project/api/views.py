from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer, MyModelSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import MyModel


# api view 
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# implementing CRUD
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer






#authentications 
class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is view is protected."})
    
class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "This is view is for admin-only."})
    

class PublicView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        return Response({"message": "This view is open to everyone."})
    

# viewset permissions
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

    permission_classes = [IsAuthenticated]  

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]  
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]  
        return super().get_permissions()




    

