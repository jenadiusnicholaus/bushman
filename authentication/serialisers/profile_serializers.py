from rest_framework import serializers
from ..models import UserProfile
import json
from django_countries.serializer_fields import CountryField
from django.contrib.auth.models import User


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
        )


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GetProfileSerializer(serializers.ModelSerializer):
    country = CountryField(country_dict=True)
    user = GetUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "date_of_birth",
            "gender",
            "photo",
            "address",
            "phone",
            "city",
            "country",
            "state",
            "created_at",
            "updated_at",
            "user",
            "passport_number",
        ]

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            country_code = representation["country"]

            representation["country"] = {
                "code": country_code,
            }

            # absolute url for photo
            if representation.get("photo"):
                representation["photo"] = representation["photo"].url
            return representation


class CreateUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"


class UpdateUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "photo": {"required": False}}
