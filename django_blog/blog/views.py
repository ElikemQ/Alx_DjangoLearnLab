from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUerChangeForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm
# Create your views here.

def register(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form':form})

    
@login_required
def profile(request):
    if request.method =='POST':
        user_form = CustomUerChangeForm(request.POST, instnce=request.user)
        profile_form = profile_form(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = CustomUerChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'blog/profile.html', {
        'user_form': user_form,
        'profile_form' : profile_form,
    })

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:postlist')
    


class PostUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = '/login/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('blog:post_list')
    
class PostDeleteView(LoginRequiredMixin, DeleteView, UserPassesTestMixin):
    model = Post
    template_name = 'blog/post_delete.html'
    login_url = '/login/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)