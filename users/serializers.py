from rest_framework import serializers

from . import models


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('phone_number', 'email')


class VerifyUserSerializer(serializers.ModelSerializer):
    session_id = serializers.UUIDField()
    code = serializers.CharField(max_length=4)

    class Meta:
        model = models.User
        fields = ('session_id', 'code')


class CreateTokenSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = models.User
        fields = ('phone_number',)


class GetUserClass(serializers.ModelSerializer):
    token = serializers.CharField()
