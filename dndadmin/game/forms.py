from django import forms

from game.models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'image']

class GameSearchForm(forms.Form):
    name = forms.CharField(label='Название', max_length=100)

class HitPointForm(forms.Form):
    value = forms.IntegerField(label="Введите значение", min_value=0)


