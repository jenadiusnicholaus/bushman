from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from authentication.serialisers.profile_serializers import ProfileSerializer
from..serialisers.global_serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from..models import UserProfile
from rest_framework import viewsets 
from django.utils import timezone



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    allowed_methods = ('POST',)

    def create(self, request, *args, **kwargs):
        data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'password2': request.data.get('password2'),
            'email': request.data.get('email'),
            'first_name': request.data.get('first_name'),   
            "last_name": request.data.get('last_name')  

        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers( serializer.data )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.get_queryset().filter(user=self.request.user).first()
        

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user).first()
       
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'bio': request.data.get('bio'),
            'gender': request.data.get('gender'),
            "date_of_birth": request.data.get('date_of_birth'), 
            'photo': request.data.get('profile_picture'),
            'phone': request.data.get('phone_number'),
            'address': request.data.get('address'),
            'city': request.data.get('city'),
            "created_at": timezone.now()
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer) 
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)




    