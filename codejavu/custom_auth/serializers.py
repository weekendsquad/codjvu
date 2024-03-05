from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class LoginSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(required=False)

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'last_login': {'required': True}
        }

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance refresh_token and last_login time
        """
        instance.last_login = validated_data.get('last_login', instance.last_login)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
