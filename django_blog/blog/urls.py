from django.urls import path
from .views import register, profile, PostCreateView, PostDeleteView, PostDetailView, PostListView, PostUpdateView, create_comment, update_comment, CommentDeleteView, CommentUpdateView, CommentCreateView
from django.contrib.auth.views import LoginView, LogoutView  
from . import views


app_name = 'blog'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view, name='create_comment'),
    path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='update_comment'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),
    
]

