from django.db import models
from django.db.models import TextChoices


class Difficulty(TextChoices):
    A1 = 'A1', 'A1'
    A2 = 'A2', 'A2'
    B1 = 'B1', 'B1'
    B2 = 'B2', 'B2'
    C1 = 'C1', 'C1'
    C2 = 'C2', 'C2'

class Language(TextChoices):
    EN = 'EN', 'EN'
    RU = 'RU', 'RU'

class Word(models.Model):
    text = models.CharField(max_length=255)
    category = models.ForeignKey('main.Category', on_delete=models.CASCADE)
    language = models.CharField(max_length=5, choices=Language.choices, default=Language.EN)
    difficulty = models.CharField(max_length=5, choices=Difficulty.choices, default=Difficulty.A1)

    def __str__(self):
        return f"{self.language} - {self.text} - {self.difficulty}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Translation(models.Model):
    language = models.CharField(max_length=5, choices=Language.choices, default=Language.EN)
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.language} - {self.text}"


class Card(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    wrong_answered = models.IntegerField(default=0)
    priority = models.FloatField(default=1)
    
    @staticmethod 
    def create(word : str, translation: str, first_language : Language, second_language : Language): # type: ignore
        new_card = Card()
        
        new_card.word = Word(text=word, language=first_language, category=Category.objects.first())
        new_card.word.save()
        
        new_card.translation = Translation(text=translation, language=second_language)
        new_card.translation.save()
        
        new_card.save()
        
        return new_card


    class Meta:
        indexes = [
            models.Index(fields=['-priority'], name='priority_desc_index'),  # Индекс для быстрого поиска
        ]

    def __str__(self):
        return f"{self.word} - {self.translation} - {self.wrong_answered}"

class CardSet(models.Model):
    name = models.CharField(max_length=255)
    first_language = models.CharField(max_length=5, choices=Language.choices, default=Language.EN)
    second_language = models.CharField(max_length=5, choices=Language.choices, default=Language.RU)
    cards = models.ManyToManyField(Card)

    def __str__(self):
        return f"{self.name} - {self.first_language} - {self.second_language}"

class Profile(models.Model):
    total_cards = models.IntegerField(default=0)
    
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    cards_sets = models.ManyToManyField(CardSet, related_name='profiles')

