from rest_framework import serializers
from .models import Suit


class SuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suit
        fields = ("url", "name", "color", "fit", "material", "image")