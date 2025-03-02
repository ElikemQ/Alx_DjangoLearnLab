from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ExampleForm
from .forms import BookSearchForm 
# Create your views here.

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """View all articles."""
    books = Book.objects.all()
    return render(request)

@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    """Create an article (requires can_create permission)."""
    if request.method == "POST":
        # Handle article creation logic
        pass
    return render(request)

@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    """Edit an article (requires can_edit permission)."""
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        # Handle article editing logic
        pass
    return render(request)

@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    """Delete an article (requires can_delete permission)."""
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return render("request")


# New View: Example Form Handling
@login_required
def example_form_view(request):
    # This view explicitly uses ExampleForm
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Do something with the form data
            return redirect('example_success')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/example_form.html', {'form': form})