from django.forms import forms, ModelForm

from characterapp.models import Character


class CharacterCreateForm(ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'dnd_class', 'race', 'background', 'max_hp', 'armor_class', 'initiative', 'is_player', 'image']
