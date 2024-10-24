from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated


from authentication.serialisers.profile_serializers import CreateUserProfileSerializer, GetProfileSerializer, GetUserSerializer, UpdateUserProfileSerializer, UpdateUserSerializer

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
    serializer_class = GetProfileSerializer

    def get_object(self):
        return self.get_queryset().filter(user=self.request.user).first()
        
    def list(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({
                "message": "User profile does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer =self.get_serializer(user_profile)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Get the user data from the request
        print(request.data)
        data = {
            "user": request.user.id,
            "date_of_birth": request.data.get('date_of_birth'),
            "gender": request.data.get('gender'),
            "photo": request.data.get('photo'),
            "address": request.data.get('address'),
            "phone": request.data.get('phone'),
            "country": request.data.get('country'),
            "city": request.data.get('city'),
            "state": request.data.get('state'),
            "passport_number": request.data.get("passport_number"),
            'created_at': timezone.now(),
        }

        # Initialize the serializer for creating a new user profile
        serializer = CreateUserProfileSerializer(data=data)

        if serializer.is_valid():
            # Create the user profile
            self.perform_create(serializer)
        
            cl, c = Client.objects.get_or_create(user=request.user)
            
            # Update user first and last name
            user_serializer = UpdateUserSerializer(request.user, data={"first_name": request.data.get('first_name'), "last_name": request.data.get('last_name')}, partial=True)
            if user_serializer.is_valid(raise_exception=True):
               user_serializer.save()
            
            return Response({
                "message": "Your profile has been created successfully"
            }, status=status.HTTP_201_CREATED)
           
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    
       
    
    def patch(self, request, *args, **kwargs):
        data = {
            "date_of_birth": request.data.get('date_of_birth', None),
            "gender": request.data.get('gender', None),
            "photo": request.data.get('photo', None),
            "address": request.data.get('address', None),
            "country": request.data.get('country'),
            "phone": request.data.get('phone', None),
            "city": request.data.get('city', None),
            "state": request.data.get('state', None),
            "passport_number": request.data.get("passport_number", None)
        }
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UpdateUserProfileSerializer(instance=user_profile, data=data, partial=True)
        
        # Validate all serializers
        if serializer.is_valid():
            self.perform_update(serializer)
            user = User.objects.get(id=request.user.id)
            cl,c=Client.objects.get_or_create(user=request.user)
            user_serializer = UpdateUserSerializer(user, data={"first_name": request.data.get('first_name', None), "last_name": request.data.get('last_name', None)}, partial=True)
            if user_serializer.is_valid(raise_exception=True):
               user_serializer.save()
        
            return Response({
                "message": "Your profile has been updated successfully"

            }, status=status.HTTP_200_OK)
        else:   
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, *args, **kwargs):
        instance = UserProfile.objects.get(user=request.user)
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Your profile has been deleted successfully"
            },
            status=status.HTTP_200_OK)




    