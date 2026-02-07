from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import generics, permissions, status, parsers
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import DndClassSerializer, DndRaceSerializer, UsernameSerializer, CharacterSerializer, \
    BackgroundSerializer, UpdateCharacterSerializer, AbilitySerializer, SkillSerializer, GameSerializer
from bookdata.models import DndClass, Race, Background
from characterapp.models import Character, Ability, Skill
from game.models import Game


class DndClassApiView(generics.ListAPIView):
    queryset = DndClass.objects.all()
    serializer_class = DndClassSerializer
    permission_classes = (permissions.IsAuthenticated, )

class DndRaceApiView(generics.ListAPIView):
    queryset = Race.objects.all()
    serializer_class = DndRaceSerializer
    permission_classes = (permissions.IsAuthenticated, )

class DndBackgroundApiView(generics.ListAPIView):
    queryset = Background.objects.all()
    serializer_class = BackgroundSerializer
    permission_classes = (permissions.IsAuthenticated, )

class GetUsernameApiView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        print(UsernameSerializer(self.request.user))
        return Response(UsernameSerializer(self.request.user).data, status=status.HTTP_200_OK)

class CharacterApiView(ListAPIView):

    serializer_class = CharacterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user).prefetch_related('abilities', 'abilities__skills')

class CharacterInsertApiView(UpdateAPIView):
    queryset = Character.objects.all()
    serializer_class = UpdateCharacterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, )
    http_method_names = ['patch']

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)

class CharacterCreateApiView(CreateAPIView):
    queryset = Character.objects.all()
    serializer_class = UpdateCharacterSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = self.request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        new_character_id = serializer.data['id']
        for ability_choice in Ability.AbilityType.choices:
            ability = Ability.objects.create(character_id=new_character_id, ability=ability_choice[0])
            ability.save()
            Skill.create_skills(ability)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AbilityUpdateApiView(UpdateAPIView):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Ability.objects.filter(character__user=self.request.user)

class SkillUpdateApiView(UpdateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Skill.objects.filter(ability__character__user=self.request.user)

class GameListApiView(ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Game.objects.filter(master=self.request.user).prefetch_related('characters', 'encounters', 'encounters__encounter_characters')