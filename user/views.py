from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.urls import reverse

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            login(request, user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse('user:activate', kwargs={'uidb64': uid, 'token': token})
            )
            
            subject = 'Подтверждение регистрации'
            message = render_to_string('user/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(request, 'Проверьте вашу почту для подтверждения регистрации.')
            return redirect('index')  
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {'form': form})

def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш аккаунт активирован. Теперь вы можете войти.')
        return redirect('user:login')
    else:
        messages.error(request, 'Ссылка активации недействительна или устарела.')
        return redirect('user:register')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, 'Аккаунт не активирован. Проверьте почту.')
                return redirect('user:login')
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('index')  

@login_required
def profile_view(request):
    return render(request, 'user/profile.html', {'user': request.user})
