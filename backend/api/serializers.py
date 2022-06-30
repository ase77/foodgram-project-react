from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import exceptions, serializers
from django.contrib.auth import authenticate
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name'
        ]


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=128)

    def validate(self, data):

        try:
            user = CustomUser.objects.get(email=data['email'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                'email незарегистрированного пользователя.'
            )
        if user.check_password(data['password']):
            return data
        raise serializers.ValidationError('Неверный пароль')
