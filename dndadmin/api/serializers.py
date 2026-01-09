from rest_framework import serializers

from bookdata.models import DndClass


class DndClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = DndClass
        fields = '__all__'


class AltDndClassSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    image = serializers.ImageField()