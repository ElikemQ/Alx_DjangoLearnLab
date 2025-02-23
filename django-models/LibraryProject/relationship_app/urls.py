from django.urls import path
from .views import list_books, LibraryDetailView 
from .views import admin_view, librarian_view, member_view
from .import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', 'relationship_app.views.register', name='register'),
    
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/',views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    ]

