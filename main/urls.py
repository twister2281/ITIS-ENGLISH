from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('learning/', views.learning, name='learning'),
    path('add_user_card/', views.add_user_card, name='add'),
    path('get_new_card_from_dict', views.get_new_card_from_dict, name='get_new'),
    path('get_cards', views.get_cards, name='get'),
    path('remove_card', views.remove_card, name='remove'),
    path('remember_card', views.remember_card, name='remember'),
    path('dont_remember_card', views.dont_remember_card, name='dont_remember'),
    path('edit_card', views.edit_card, name='edit'),
    path('my-words/', views.my_words_view, name='my_words'),
]
