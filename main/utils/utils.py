from django.http import JsonResponse
from main.models import Card, Profile


class MasterCard:
    
    @staticmethod
    def pack(cards: list[Card]):
        data = {
            "cards_buffer": []
        }

        for card in cards:
            data["cards_buffer"].append({
                "word": card.word.text,
                "translation": card.translation.text,
                "id": card.id
                })
        return data 
    
    @staticmethod
    def dont_remember_card(profile_id : int, card_id: int):
        profile = Profile.objects.get(id = profile_id)
        profile.total_cards += 1
        profile.save()
        
        cards_set = profile.cards_sets.first()
        
        cur_card = cards_set.cards.get(id=card_id)
        cur_card.wrong_answered += 1
        cur_card.priority = profile.total_cards - cur_card.wrong_answered * 10
        cur_card.save()
        
        return JsonResponse({})
    
    @staticmethod
    def remember_card(profile_id : int, card_id : int):
        profile = Profile.objects.get(id = profile_id)
        profile.total_cards += 1
        
        cards_set = profile.cards_sets.first()
        
        cur_card = cards_set.cards.get(id=card_id)
        cur_card.wrong_answered -= 1
        cur_card.priority = profile.total_cards - cur_card.wrong_answered * 10
        cur_card.save()
        
        return JsonResponse({})
    
    @staticmethod
    def remove_card(profile_id : int, card_id : int):
        profile = Profile.objects.get(id = profile_id)
        
        cards_set = profile.cards_sets.first()
        
        cur_card = cards_set.cards.get(id=card_id)
        cards_set.cards.remove(cur_card)
        
        return JsonResponse({})
    
    @staticmethod
    def get_new_card_from_dict(profile_id : int):
        print('получить новую карточку')
        return JsonResponse({})
    
    @staticmethod
    def get_most_beautiful_cards(profile_id : int, n : int) -> Card:
        profile = Profile.objects.get(id = profile_id)
        
        return MasterCard.pack(profile.cards_sets.first().cards.order_by('priority')[:n])
    
    @staticmethod
    def get_cards(profile_id : int, buffer_size : int):        
        return MasterCard.get_most_beautiful_cards(profile_id, buffer_size)
    
    @staticmethod
    def add_user_card(profile_id : int, word : str, translation : str) -> JsonResponse:
        profile = Profile.objects.get(id = profile_id)
        cards_set = profile.cards_sets.first()
        first_language, second_language = cards_set.first_language, cards_set.second_language
        
        new_card = Card.create(word, translation, first_language, second_language)
        
        cards_set.cards.add(new_card)
        
        return MasterCard.pack([new_card])

    @staticmethod
    def edit_card(profile_id : int, word : str, translation : str, card_id : str) -> JsonResponse:
        profile = Profile.objects.get(id = profile_id)
        cards_set = profile.cards_sets.first()
        
        ed_card = cards_set.cards.get(id=card_id)
        ed_card.word.text = word
        ed_card.translation.text = translation
                
        ed_card.word.save()
        ed_card.translation.save()
        ed_card.save()
        
        return MasterCard.pack([ed_card])
