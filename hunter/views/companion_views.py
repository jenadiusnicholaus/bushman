from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from hunter.models import Client, Companion, Observer
from hunter.serializers.companion_sz import (
    CreateCompanionClientSerializer,
    GetCompanionClientSerializer,
    UpdateCompanionClientSerializer,
)

from authentication.serialisers.profile_serializers import (
    CreateUserSerializer,
    CreateUserProfileSerializer,
    UpdateUserProfileSerializer,
    UpdateUserSerializer,
)
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


class ClientCompanionsViewSets(viewsets.ModelViewSet):
    serializer_class = GetCompanionClientSerializer
    queryset = Companion.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        companion_id = self.request.query_params.get("companion_id")
        if companion_id:
            try:
                companionObj = Companion.objects.get(id=companion_id)
                serializer = self.get_serializer(companionObj)
                return Response(serializer.data)
            except:
                return Response({"message": "Companion not found"}, status=404)

        else:
            queryset = self.get_queryset().filter(client__user=request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            client_id = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return Response({"message": "Client not found"}, status=404)

        password = self.randPassword()
        user_data = {
            "username": request.data.get("email"),
            "password": password,
            "password2": password,
            "email": request.data.get("email"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
        }

        user_serializer = CreateUserSerializer(data=user_data)

        # Validate the user serializer
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=400)

        # Prepare companion profile data but don't save yet
        companion_profile_data = {
            "user": None,  # Temporary placeholder
            "date_of_birth": request.data.get("date_of_birth"),
            "gender": request.data.get("gender"),
            "photo": request.data.get("photo"),
            "address": request.data.get("address"),
            "phone": request.data.get("phone"),
            "country": request.data.get("country"),
            "city": request.data.get("city"),
            "state": request.data.get("state"),
            "passport_number": request.data.get("passport_number"),
            "created_at": timezone.now(),
        }

        companion_profile_serializer = CreateUserProfileSerializer(
            data=companion_profile_data
        )

        # Validate the profile serializer
        if not companion_profile_serializer.is_valid():
            return Response(companion_profile_serializer.errors, status=400)

        # Prepare companion data but don't save yet
        companion_data = {
            "client": client_id.id,
            "user": None,  # Temporary placeholder
            "created_at": timezone.now(),
        }

        companion_serializer = CreateCompanionClientSerializer(data=companion_data)

        # Validate companion serializer
        if not companion_serializer.is_valid():
            return Response(companion_serializer.errors, status=400)

        # Now that all serializers are valid, let's save them
        with transaction.atomic():  # Start a transaction
            companion_user = user_serializer.save()  # Save user
            companion_profile_data["user"] = (
                companion_user.id
            )  # Set the user ID in profile data

            # Create a new instance of the profile serializer with updated data
            companion_profile_serializer = CreateUserProfileSerializer(
                data=companion_profile_data
            )

            # Validate and save the profile serializer
            if not companion_profile_serializer.is_valid():
                user = User.objects.get(id=companion_user.id)
                user.delete()  # Delete the user if profile serializer is invalid

                return Response(companion_profile_serializer.errors, status=400)
            companion_profile = companion_profile_serializer.save()  # Save profile

            companion_data["user"] = (
                companion_user.id
            )  # Set the user ID in companion data

            # Create a new instance of the companion serializer with updated data
            companion_serializer = CreateCompanionClientSerializer(data=companion_data)

            # Validate and save the companion serializer
            if not companion_serializer.is_valid():
                return Response(companion_serializer.errors, status=400)
            companion_serializer.save()  # Save companion data

        return Response(
            {
                "message": "Companion created successfully",
            },
            status=201,
        )

    def patch(self, request, *args, **kwargs):
        observer_id = self.request.query_params.get("companion_id")
        # observer = Observer.objects.get(id=observer_id)
        try:
            compaion = Companion.objects.get(id=observer_id)
        except:
            return Response({"message": "Companion not found"}, status=404)

        try:
            user = User.objects.get(id=compaion.user.id)
        except:
            return Response({"message": "User not found"}, status=404)

        profile = compaion.user.profile
        user_data = {
            "username": request.data.get("username", user.username),
            "email": request.data.get("email", user.email),
            "first_name": request.data.get("first_name", user.first_name),
            "last_name": request.data.get("last_name", user.last_name),
        }
        user_serializer = UpdateUserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            observer_profile_data = {
                "date_of_birth": request.data.get(
                    "date_of_birth", profile.date_of_birth
                ),
                "gender": request.data.get("gender", profile.gender),
                "photo": request.data.get("photo", profile.photo),
                "address": request.data.get("address", profile.address),
                "phone": request.data.get("phone", profile.phone),
                "city": request.data.get("city", profile.city),
                "state": request.data.get("state", profile.state),
                "passport_number": request.data.get(
                    "passport_number", profile.passport_number
                ),
                "updated_at": timezone.now(),
            }
            ob_profiele_serializer = UpdateUserProfileSerializer(
                profile, data=observer_profile_data, partial=True
            )
            if ob_profiele_serializer.is_valid():
                ob_profile = ob_profiele_serializer.save()
                observer_data = {
                    "client": compaion.client.id,
                    "user": compaion.user.id,
                    "updated_at": timezone.now(),
                }
                observer_serializer = UpdateCompanionClientSerializer(
                    compaion, data=observer_data, partial=True
                )
                if observer_serializer.is_valid():
                    observer_serializer.save()
                    return Response(
                        {
                            "message": "Companion updated successfully",
                        },
                        status=200,
                    )
                else:
                    return Response(observer_serializer.errors, status=400)
            else:
                return Response(ob_profiele_serializer.errors, status=400)
        else:
            return Response(user_serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        companion_id = self.request.query_params.get("companion_id")
        try:
            companion = Companion.objects.get(id=companion_id)
        except:
            return Response({"message": "Companion not found"}, status=404)
        user = companion.user
        profile = user.profile
        user.delete()
        profile.delete()
        companion.delete()
        return Response({"message": "Companion deleted successfully"}, status=200)

    def randPassword(self):
        import random
        import string

        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(10))
