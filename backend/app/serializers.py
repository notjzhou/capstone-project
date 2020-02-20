from rest_framework import serializers
from .models import Beat, Rap


class BeatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'file',
            'bpm',
        )
        model = Beat


class RapSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'recording',
            'bpm',
        )
        model = Rap
