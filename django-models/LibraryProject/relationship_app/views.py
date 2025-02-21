from django.shortcuts import render

# Create your views here.
from .models import Book 

def list_books(request):
    books = Book.objects.all()

    return render(request, 'relationship_app/list_books.html', {'books': books})


from django.views.generic import ListView
from .models import Library, Book

class LibraryBookListView(ListView):
    model = Book
    template_name = 'relationship_app/library_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        library_id = self.kwargs['library_id']
        return Book.objects.filter(library__id=library_id)
