from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import generics, permissions, status, parsers
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import DndClassSerializer, DndRaceSerializer, UsernameSerializer, CharacterSerializer, \
    BackgroundSerializer, UpdateCharacterSerializer, AbilitySerializer, SkillSerializer
from bookdata.models import DndClass, Race, Background
from characterapp.models import Character, Ability, Skill


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

    def get_queryset(self):
        return Character.objects.filter(user=self.request.user)

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