from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUerChangeForm, ProfileForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from taggit.models import Tag





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
    

@login_required
def create_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)  
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post 
            comment.save()  
            return redirect('blog:post_detail', pk=post.pk) 
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})


@login_required
def update_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return redirect('blog:post_detail', pk=comment.post.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form': form, 'comment': comment})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all() 
        context['comment_form'] = CommentForm()
        return context


# @login_required
# def create_comment(request, post_pk):
#     post = get_object_or_404(Post, pk=post_pk) 
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user 
#             comment.post = post 
#             comment.save() 
#             return redirect('blog:post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return redirect('blog:post_detail', pk=post.pk) 

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    context_object_name = 'comment'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author 

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    

def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter (Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)).distinct()
    else:
        posts = Post.objects.all()
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})



class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)