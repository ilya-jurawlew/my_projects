from rest_framework import serializers

from app_animals.models import Animals, Shelter


class AnimalsSerializers(serializers.ModelSerializer):
    """Сериализатор животных"""
    class Meta:
        model = Animals
        fields = '__all__'


class ShelterSerializers(serializers.ModelSerializer):
    """Сериализатор приютов"""
    class Meta:
        model = Shelter
        fields = '__all__'
