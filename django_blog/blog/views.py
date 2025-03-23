from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUerChangeForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserChangeForm
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


# @login_required
# def profile(request):
#     if request.method =='POST':
#         form = UserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('proflie')
#         else:
#             form = UserChangeForm(instance=request.user)
#         return render(request, 'blog/profile.html', {'form' : form})
    
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