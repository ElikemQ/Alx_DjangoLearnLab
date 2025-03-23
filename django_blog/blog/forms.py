from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

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