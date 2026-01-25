from django.contrib.auth import get_user_model
from rest_framework import serializers


from bookdata.models import DndClass, Race, Background
from characterapp.models import Character, Skill, Ability


class DndClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = DndClass
        fields = '__all__'

class DndRaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = '__all__'

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username',)

class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = '__all__'



class SkillSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()

    def get_skill(self, obj):
        return {"name": obj.get_skill_display(), 'choice': obj.skill}

    class Meta:
        model = Skill
        fields = ('id', 'skill', 'value', 'is_proficient')

class AbilitySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    ability = serializers.SerializerMethodField()

    def get_ability(self, obj):
        return {'name': obj.get_ability_display(), 'choice': obj.ability}

    class Meta:
        model = Ability
        fields = ('id', 'ability', 'value', 'is_proficient', 'saving_throw', 'skills')

class CharacterSerializer(serializers.ModelSerializer):
    abilities = AbilitySerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = ('id', 'name', 'dnd_subclass', 'max_hp', 'hp', 'armor_class', 'initiative', 'cooper_coins', 'silver_coins',
                  'gold_coins', 'is_player', 'image', 'level', 'speed', 'proficient_bonus', 'dnd_class', 'race', 'background',
                  'abilities')


class UpdateCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'name', 'dnd_subclass', 'max_hp', 'hp', 'armor_class', 'initiative', 'cooper_coins',
                  'silver_coins', 'gold_coins', 'level', 'speed', 'proficient_bonus', 'dnd_class', 'race',
                  'background', 'image')


