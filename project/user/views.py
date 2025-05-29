# user/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from main.models import Profile


from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.is_active = False 
            user.save()

            send_mail(
                subject='Подтверждение регистрации',
                message='Спасибо за регистрацию! (Здесь должна быть ссылка подтверждения)',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            messages.success(request, 'Проверьте почту для подтверждения.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'user/profile.html', {'user': request.user})
