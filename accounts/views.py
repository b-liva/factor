from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from accounts.forms import EditProfileForm, PassChangeForm

# Create your views here.


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('allTables')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Password must match'})

    else:
        pass
        return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, level=20, message='مشخصات کاربری بروزرسانی شد.')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


@login_required
def profile(request):
    user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PassChangeForm(data=request.POST or None, user=request.user)

        if form.is_valid():
            form.save()
            messages.add_message(request, level=20, message='پسوورد با موفقیت بروزرسانی شد.')
            return redirect('profile')
    else:
        form = PassChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)
