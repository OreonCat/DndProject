from django.forms import model_to_dict
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import DndClassSerializer, DndRaceSerializer
from bookdata.models import DndClass, Race


class DndClassApiView(generics.ListAPIView):
    queryset = DndClass.objects.all()
    serializer_class = DndClassSerializer
    permission_classes = (permissions.IsAuthenticated, )

class DndRaceApiView(generics.ListAPIView):
    queryset = Race.objects.all()
    serializer_class = DndRaceSerializer
    permission_classes = (permissions.IsAuthenticated, )
