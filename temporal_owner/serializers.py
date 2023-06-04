from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from rest_framework import serializers
from .models import TemporalOwner
from django.contrib.auth import get_user_model
from typing import Dict, Any
from rest_framework.authtoken.models import Token


class TemporalOwnerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(10),
            RegexValidator(
                regex=r'^(?=.*\d)(?=.*[a-z]{2,})(?=.*[A-Z])[0-9a-zA-Z]{6,10}$',
                message="Password must contain at least one digit, "
                        "two lowercase letters, one uppercase letter, and no other special characters."
            )
        ]
    )

    class Meta:
        model = get_user_model()
        fields = ("id", 'first_name', 'last_name', 'city', 'username', 'password')
        read_only_fields = ("id", 'is_admin', 'is_superuser', "is_staff")
        write_only_fields = "password"

    def create(self, validated_data: Dict[str, Any]) -> get_user_model():
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username")
    password = serializers.CharField(label="Password", style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            try:
                user = TemporalOwner.objects.get(username=username)
            except TemporalOwner.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials.")

            if user.check_owner_password(password):
                token, _ = Token.objects.get_or_create(user=user)
                attrs["user"] = user
                attrs["token"] = token
                return attrs
            else:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Username and password are required.")