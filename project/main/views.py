from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render



from main.utils.utils import MasterCard
from main.models import Profile

def get_user_profile(request) -> Profile:
    if not request.user.is_authenticated:
        return HttpResponse("You must be authorized to access this page", status=401)
    
    return request.user.profile

def dont_remember_card(request):
    profile = get_user_profile(request)
    
    return MasterCard.dont_remember_card(profile.id, request.POST.get('card_id'))

def remember_card(request):
    profile = get_user_profile(request)
    
    return MasterCard.remember_card(profile.id, request.POST.get('card_id'))

def remove_card(request):
    profile = get_user_profile(request)
    
    return MasterCard.remove_card(profile.id, request.POST.get('card_id'))

def get_cards(request):
    profile = get_user_profile(request)
    
    data = MasterCard.get_cards(profile.id, request.POST.get('number'))
    return JsonResponse(data, safe=False)

def get_new_card_from_dict(request):
    profile = get_user_profile(request)
    
    return MasterCard.get_new_card_from_dict(profile.id)

def add_user_card(request):
    profile = get_user_profile(request)
    
    data = MasterCard.add_user_card(profile.id, request.POST.get('word'), request.POST.get('translation'))
    return JsonResponse(data)

def edit_card(request):
    profile = get_user_profile(request)
    
    data = MasterCard.edit_card(profile.id, request.POST.get('word'), request.POST.get('translation'), request.POST.get('card_id'))
    return JsonResponse(data)


def learning(request):
    return render (request, 'main/learning.html')

def index(request):
    return render (request, 'main/index.html')

def about(request):
    pass

def logout_site(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


def login_site(request):
    if request.user.is_authenticated:
        return redirect('index')
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            message = 'Извините, такого пользователя не существует'
            return render(request, 'main/login.html', {'message': message})
    return render(request, 'main/login.html', {'message': message})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'main/index.html')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form':form})
	


def index(request):
    return render(request, 'main/index.html')
