from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import DndClassSerializer, DndRaceSerializer, UsernameSerializer, CharacterSerializer
from bookdata.models import DndClass, Race
from characterapp.models import Character


class DndClassApiView(generics.ListAPIView):
    queryset = DndClass.objects.all()
    serializer_class = DndClassSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return DndClass.objects.exclude(name="Отсутствует")

class DndRaceApiView(generics.ListAPIView):
    queryset = Race.objects.all()
    serializer_class = DndRaceSerializer
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
