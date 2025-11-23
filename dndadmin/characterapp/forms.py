from django import forms

from bookdata.models import DndClass, Race
from characterapp.models import Character


class CharacterCreateForm(forms.ModelForm):
    level = forms.IntegerField(min_value=1, label="Уровень")
    max_hp = forms.IntegerField(min_value=0, label="Max HP")
    initiative = forms.IntegerField(min_value=0, label="Инициатива")
    armor_class = forms.IntegerField(min_value=0, label="КД")
    speed = forms.IntegerField(min_value=0, label="Скорость")
    image = forms.ImageField(required=False, widget=forms.FileInput)
    class Meta:
        model = Character
        fields = ['name', 'dnd_class', 'dnd_subclass', 'race', 'level', 'background', 'max_hp', 'armor_class', 'initiative', 'is_player', 'image', 'speed']

class CoinForm(forms.ModelForm):
    cooper_coins = forms.IntegerField(min_value=0, label="Медные монеты")
    silver_coins = forms.IntegerField(min_value=0, label="Серебряные монеты")
    gold_coins = forms.IntegerField(min_value=0, label="Золотые монеты")
    class Meta:
        model = Character
        fields = ['cooper_coins', 'silver_coins', 'gold_coins']


class SearchForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=100, required=False)
    dnd_class = forms.ModelChoiceField(queryset=DndClass.objects.all(), label="Класс", required=False)
    race = forms.ModelChoiceField(queryset=Race.objects.all(), label="Раса", required=False)
    level = forms.IntegerField(min_value=1, required=False, label="Уровень")