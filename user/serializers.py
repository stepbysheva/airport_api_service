from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "email", "password", "is_staff"
        extra_kwargs = {"password": {"write_only": True}, "is_staff": {"read_only": True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        new_instance = super().update(instance, validated_data)
        if password:
            new_instance.set_password(password)
            new_instance.save()
        return new_instance
