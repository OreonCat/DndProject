from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookdata.models import DndClass, Race
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



class SkillSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()

    def get_skill(self, obj):
        return obj.get_skill_display()

    class Meta:
        model = Skill
        fields = ('id', 'skill', 'value', 'is_proficient')


class AbilitySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    ability = serializers.SerializerMethodField()

    def get_ability(self, obj):
        return obj.get_ability_display()

    class Meta:
        model = Ability
        fields = ('id', 'ability', 'value', 'is_proficient', 'saving_throw', 'skills')

class CharacterSerializer(serializers.ModelSerializer):
    abilities = AbilitySerializer(many=True, read_only=True)
    dnd_class = serializers.SerializerMethodField()
    race = serializers.SerializerMethodField()
    background = serializers.SerializerMethodField()

    def get_dnd_class(self, obj):
        return obj.dnd_class.name

    def get_race(self, obj):
        return obj.race.name

    def get_background(self, obj):
        return obj.background.name

    class Meta:
        model = Character
        fields = ('id', 'name', 'dnd_subclass', 'max_hp', 'hp', 'armor_class', 'initiative', 'cooper_coins', 'silver_coins',
                  'gold_coins', 'is_player', 'image', 'level', 'speed', 'proficient_bonus', 'dnd_class', 'race', 'background',
                  'abilities')


