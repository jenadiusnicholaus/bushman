from rest_framework import serializers

from authentication.serialisers.profile_serializers import (
    GetProfileSerializer,
    GetUserSerializer,
)
from hunter.models import Observer


class GetObserverClientSerializer(serializers.ModelSerializer):
    user = GetUserSerializer()
    user_profile = serializers.SerializerMethodField()

    def get_user_profile(self, obj):
        try:
            profile = obj.user.profile
            serializer = GetProfileSerializer(profile, context=self.context)
            profile_data = serializer.data

            # Modify the photo URL to be absolute
            request = self.context.get("request")  # Get the request context
            if "photo" in profile_data and profile_data["photo"]:
                profile_data["photo"] = request.build_absolute_uri(
                    profile_data["photo"]
                )  # Create absolute URL

            return profile_data
        except:
            return None

    class Meta:
        model = Observer
        fields = "__all__"


class CreateObserverClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observer
        fields = "__all__"


class UpdateObserverClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observer
        fields = "__all__"
