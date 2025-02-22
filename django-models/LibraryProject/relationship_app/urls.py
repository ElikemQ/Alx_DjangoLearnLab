from django.urls import path
from .views import list_books, LibraryDetailView
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    

    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", auth_views.TemplateView.as_view(template_name="registration_app/home.html"), name="home")
    
    
    
    ]

