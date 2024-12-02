from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileUpdateForm
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('profile')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/update_profile.html', {'form': form})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=request.user.pk)
        user.delete()
        messages.success(request, "Your profile has been deleted.")
        return redirect('login')
    return render(request, 'users/delete_profile.html')