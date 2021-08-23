from rest_framework import serializers

from app_users.models import Profile
from app_animals.models import Shelter


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя"""
    username = serializers.CharField(max_length=50, min_length=4)
    password = serializers.CharField(max_length=150, min_length=6, write_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'password', 'city', 'phone', 'shelter']

    def validate(self, request):
        username = request.get('username', None)
        if Profile.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Bad username'})
        return super().validate(request)

    def create(self, validated_data):
        return Profile.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['password']


class ShelterSerializer(serializers.ModelSerializer):
    """Сериализатор Приюта"""
    class Meta:
        model = Shelter
        fields = ['name']


class UserSmallSerializer(serializers.ModelSerializer):
    """Краткий Сериализатор пользователя"""
    shelter = ShelterSerializer()

    class Meta:
        model = Profile
        fields = ['username', 'city', 'phone', 'shelter']
