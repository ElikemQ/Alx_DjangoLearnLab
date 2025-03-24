from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment
from django.core.exceptions import ValidationError
from taggit.forms import TagField 
from django.forms import widgets

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
            model = User
            fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class CustomUerChangeForm(UserChangeForm):
      email = forms.EmailField(required=True)

      class Meta:
            model = User
            fields = ('username', 'email', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
      class Meta:
            model = Profile
            fields = ('bio', 'profile_picture')


class TagWidget(widgets.TextInput):
     def render(self, name, value, attrs=None, renderer=None):
          if isinstance(value,str):
               value = value.split(",")
          value = ",".join(value)
          return super().render(name, value, attrs, renderer)

class PostForm(forms.ModelForm):
      tags = forms.CharField(required=False, widget=TagWidget())

      class Meta:
            model = Post
            fields = ['title', 'content', 'tags']

      
      
      def clean_title(self):
            title = self.cleaned_data.get('title')
            if Post.objects.filter(title=title).exists():
                  raise ValidationError('This title already exist on a different post.')
            return title

      def save(self, commit=True):
            post = super().save(commit=False)
            if commit:
                  post.author = self.request.user
                  post.save()
            return post
      
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment here...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content.strip():
            raise forms.ValidationError("Comment cannot be empty.")
        return content