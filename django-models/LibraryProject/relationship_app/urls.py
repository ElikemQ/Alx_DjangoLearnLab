from django.urls import path
from .views import list_books, LibraryBookListView

urlpatterns = [
    path('books/', list_books, name='list_books'),  

    path('library/<int:library_id>/books/', LibraryBookListView.as_view(), name='library_books'),
]
