from django.shortcuts import render

# Create your views here.
from .models import Book
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.detail import DetailView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.auth import authenticate

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


def check_role(user, role):
    if not user.userprofile:
        raise PermissionDenied("User profile does not exist.")
    if user.userprofile.role != role:
        raise PermissionDenied(f"You do not have {role} privileges.")
    return True

def is_admin(user):
    return check_role(user, 'Admin')

def is_librarian(user):
    return check_role(user, 'Librarian')

def is_member(user):
    return check_role(user, 'Member')

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')