from django.contrib import admin

from .models import Word, Category, Card, CardSet, Translation, Profile

admin.site.register([Word, Category, Card, CardSet, Translation, Profile])
