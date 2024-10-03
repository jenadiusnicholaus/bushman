from rest_framework import permissions
from django.contrib.auth.models import User


class IsValidLogin(permissions.BasePermission):
    """
    Custom permission to only allow clients who are the owner of the object.
    """

    def has_permission(self, request, view):
        try:
            user = User.objects.get(id=request.user.id)
            if user.is_active:
                return True
            else:
                return False
        except User.DoesNotExist:
            return False

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name='admin').exists() and request.user.is_staff:
             return True
        else:
            return False
        
class isHunter(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name='hunter').exists() and request.user.is_staff:
             return True
        else:
            return False