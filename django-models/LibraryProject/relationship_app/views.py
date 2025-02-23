from django.shortcuts import render

# Create your views here.
from .models import Book
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.generic.detail import DetailView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib import messages
from .models import Book, Library, UserProfile, Author


def list_books(request):
    books = Book.objects.all()

    return render(request, "relationship_app/list_books.html", {"books": books})





class LibraryDetailView(DetailView):
    model = Book
    template_name = "relationship_app/library_detail.html"
    context_object_name = "books"

    def get_queryset(self):
        library_id = self.kwargs["library_id"]
        return Book.objects.filter(library__id=library_id)



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role =='Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")





# def check_role(user, role):
#     if not user.userprofile:
#         raise PermissionDenied("User profile does not exist.")
#     if user.userprofile.role != role:
#         raise PermissionDenied(f"You do not have {role} privileges.")
#     return True

# @user_passes_test(lambda u: u.userprofile.role == 'Admin')
# def admin_view(request):
#     return render(request, 'admin_view.html')

# # Librarian view - only accessible to users with the 'Librarian' role
# @user_passes_test(lambda u: u.userprofile.role == 'Librarian')
# def librarian_view(request):
#     return render(request, 'librarian_view.html')

# # Member view - only accessible to users with the 'Member' role
# @user_passes_test(lambda u: u.userprofile.role == 'Member')
# def member_view(request):
#     return render(request, 'member_view.html')

# def is_admin(user):
#     return user.userprofile.role == 'Admin'

# def is_librarian(user):
#     return user.userprofile.role == 'Librarian'

# def is_member(user):
#     return user.userprofile.role == 'Member'

# @user_passes_test(is_admin)
# def admin_view(request):
#     return render(request, 'relationship_app/admin_view.html')

# @user_passes_test(is_librarian)
# def librarian_view(request):
#     return render(request, 'relationship_app/librarian_view.html')

# @user_passes_test(is_member)
# def member_view(request):
#     return render(request, 'relationship_app/member_view.html')


@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            author = get_object_or_404(Author, id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('list_books')  
    authors = Author.objects.all()  
    return render(request, "relationship_app/add_book.html", {"authors": authors})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')
        if author_id:
            book.author = get_object_or_404(Author, id=author_id)
        book.save()
        return redirect('list_books')  
    authors = Author.objects.all()  
    return render(request, "relationship_app/edit_book.html", {"book": book, "authors": authors})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('list_books')  
    return render(request, "relationship_app/delete_book.html", {"book": book})


# @permission_required('relationship_app.can_add_book')
# def add_book(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Book added successfully!')
#             return redirect('list_books')
#     else:
#         form = BookForm()
#     return render(request, 'relationship_app/add_book.html', {'form': form})

# # View to edit an existing book
# @permission_required('relationship_app.can_change_book')
# def edit_book(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     if request.method == 'POST':
#         form = BookForm(request.POST, instance=book)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Book updated successfully!')
#             return redirect('list_books')
#     else:
#         form = BookForm(instance=book)
#     return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

# # View to delete a book
# @permission_required('relationship_app.can_delete_book')
# def delete_book(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     if request.method == 'POST':
#         book.delete()
#         messages.success(request, 'Book deleted successfully!')
#         return redirect('list_books')
#     return render(request, 'relationship_app/delete_book.html', {'book': book})