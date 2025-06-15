from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from main.utils.utils import MasterCard
from main.models import Profile


from django.contrib.auth.decorators import login_required
from .models import CardSet, Word

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


@login_required
def my_words_view(request):
    # Получаем наборы карточек пользователя
    card_sets = CardSet.objects.filter(profiles__user=request.user)
    
    # Получаем все слова пользователя
    words = Word.objects.filter(card__cardset__profiles__user=request.user).distinct()
    
    context = {
        'card_sets': card_sets,
        'words': words,
    }
    return render(request, 'user/my_words.html', context)