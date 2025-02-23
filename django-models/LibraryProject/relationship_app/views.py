from django.shortcuts import render

# Create your views here.
from .models import Book


def list_books(request):
    books = Book.objects.all()

    return render(request, "relationship_app/list_books.html", {"books": books})


from django.views.generic.detail import DetailView
from .models import Library, Book


class LibraryDetailView(DetailView):
    model = Book
    template_name = "relationship_app/library_detail.html"
    context_object_name = "books"

    def get_queryset(self):
        library_id = self.kwargs["library_id"]
        return Book.objects.filter(library__id=library_id)


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


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


from django.contrib.auth.decorators import user_passes_test
from .models import Library, Book, UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect


def is_librarian(user):
    if hasattr(user, "userprofile") and user.userprofile:
        return user.userprofile.role == "librarian"
    return False


def is_member(user):
    if hasattr(user, "userprofile") and user.userprofile:
        return user.userprofile.role == "member"
    return False


def is_admin(user):
    if hasattr(user, "userprofile") and user.userprofile:
        print(f"User role: {user.userprofile.role}")
        return user.userprofile.role == "admin"
    return False


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
