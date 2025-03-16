from rest_framework import generics, status
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from datetime import datetime

# Create your views here.

# list view for retrieving all books 
class BookListView(ListAPIView):
    queryset = Book.objects.all()  
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  


# detail view for retrieving a single book by ID
class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()  
    serializer_class = BookSerializer  
    lookup_field = 'id'  
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

#create view for adding a new book 
class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()  
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        publication_year = request.data.get('publication_year')
        if publication_year and publication_year > datetime.now().year:
            return Response({"detail": "Publication year cannot be further than today."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    

#update view for modifying an existing book
class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()  
    serializer_class = BookSerializer
    lookup_field = 'pk' 
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        book = self.get_object()
        user = self.request.user
        if book.author !=user:
            return Response({"detail": "You don't have permission to update this book."},
                            status=status.HTTP_403_FORBIDDEN) 
        
        serializer.save()

    def update(self, request, *args, **kwargs):
        publication_year = request.data.get('publication_year')
        if publication_year and publication_year > datetime.now().year:
            return Response({"detail": "Publiation year cannot be further than today"}, 
            status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

#delete view for removing book
class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()  
    serializer_class = BookSerializer  
    lookup_field = 'pk'  
    permission_classes = [IsAuthenticated]
