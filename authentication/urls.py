
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.global_views import RegisterView, UserProfileViewSet
from rest_framework import routers  
from django.urls import include

router = routers.DefaultRouter()
router.register(r'users-profile', UserProfileViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),



]