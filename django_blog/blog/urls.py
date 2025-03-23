from django.urls import path
from .views import register, profile, PostCreateView, PostDeleteView, PostDetailView, PostListView, PostUpdateView
from django.contrib.auth.views import LoginView, LogoutView  


app_name = 'blog'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
]

