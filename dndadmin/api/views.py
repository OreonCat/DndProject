from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import DndClassSerializer, AltDndClassSerializer
from bookdata.models import DndClass


class DndClassApiView(generics.ListAPIView):
    queryset = DndClass.objects.all()
    serializer_class = AltDndClassSerializer

#class DndClassApiView(APIView):
#    def get(self, request):
#        lst = DndClass.objects.all().values()
#        return Response(list(lst))
#
#    def post(self, request):
#        class_new = DndClass(name=request.data['name'])
#        return Response({'ok': model_to_dict(class_new)})