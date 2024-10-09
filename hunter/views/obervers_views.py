from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from hunter.models import Client, Observer
from hunter.serializers.observer_sz import (
    GetObserverClientSerializer,
    CreateObserverClientSerializer,
)
from authentication.serialisers.profile_serializers import (
    CreateUserSerializer,
    CreateUserProfileSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction


class ClientObserversViewSets(viewsets.ModelViewSet):
    serializer_class = GetObserverClientSerializer
    queryset = Observer.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        observer_id = self.request.query_params.get("observer_id")
        if observer_id:
            try:
                observerObj = Observer.objects.get(id=observer_id)
                serializer = self.get_serializer(observerObj)
                return Response(serializer.data)
            except:
                return Response({"message": "Observer not found"}, status=404)

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

        # Prepare observer profile data
        observer_profile_data = {
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

        # Create profile serializer initially (without validation)
        ob_profile_serializer = CreateUserProfileSerializer(data=observer_profile_data)

        # Prepare observer data
        observer_data = {
            "client": client_id.id,
            "user": None,  # Temporary placeholder
            "created_at": timezone.now(),
        }

        observer_serializer = CreateObserverClientSerializer(data=observer_data)

        # Validate observer serializer
        if not observer_serializer.is_valid():
            return Response(observer_serializer.errors, status=400)

        # All serializers is valid, save them in a transaction
        with transaction.atomic():

            observer_user = user_serializer.save()  # Save user
            observer_profile_data["user"] = observer_user.id  # Update profile user id

            # Validate and save the observer profile serializer
            ob_profile_serializer = CreateUserProfileSerializer(
                data=observer_profile_data
            )  # Reinitialize with user ID
            if not ob_profile_serializer.is_valid():  # Validate before saving
                user = User.objects.get(id=observer_user.id)
                user.delete()  # Delete the user if profile is not valid
                return Response(ob_profile_serializer.errors, status=400)
            ob_profile_serializer.save()  # Save the profile

            observer_data["user"] = observer_user.id  # Update observer user id
            observer_serializer = CreateObserverClientSerializer(
                data=observer_data
            )  # Reinitialize with user ID
            if not observer_serializer.is_valid():  # Validate before saving
                return Response(observer_serializer.errors, status=400)
            observer_serializer.save()  # Save observer

        return Response(
            {
                "message": "Observer created successfully",
                "observer": observer_serializer.data,
            },
            status=201,
        )

    def patch(self, request, *args, **kwargs):
        observer_id = self.request.query_params.get("observer_id")
        # observer = Observer.objects.get(id=observer_id)
        try:
            observer = Observer.objects.get(id=observer_id)
        except:
            return Response({"message": "Observer not found"}, status=404)

        try:
            user = User.objects.get(id=observer.user.id)
        except:
            return Response({"message": "User not found"}, status=404)

        profile = observer.user.profile
        user_data = {
            "username": request.data.get("username", user.username),
            "email": request.data.get("email", user.email),
            "first_name": request.data.get("first_name", user.first_name),
            "last_name": request.data.get("last_name", user.last_name),
        }
        user_serializer = CreateUserSerializer(user, data=user_data, partial=True)
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
            ob_profiele_serializer = CreateUserProfileSerializer(
                profile, data=observer_profile_data, partial=True
            )
            if ob_profiele_serializer.is_valid():
                ob_profile = ob_profiele_serializer.save()
                observer_data = {
                    "client": observer.client.id,
                    "user": observer.user.id,
                    "updated_at": timezone.now(),
                }
                observer_serializer = CreateObserverClientSerializer(
                    observer, data=observer_data, partial=True
                )
                if observer_serializer.is_valid():
                    observer_serializer.save()
                    return Response(
                        {
                            "message": "Observer updated successfully",
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
        observer_id = self.request.query_params.get("observer_id")
        try:

            observer = Observer.objects.get(id=observer_id)
        except:
            return Response({"message": "Observer not found"}, status=404)
        profile = observer.user.profile
        user = observer.user
        user.delete()
        profile.delete()
        observer.delete()
        return Response({"message": "Observer deleted successfully"}, status=200)

    def randPassword(self):
        import random
        import string

        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(10))
