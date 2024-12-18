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
        if request.user.groups.filter(name="admin").exists() and request.user.is_staff:
            return True
        else:
            return False


# accountant
class isAccountant(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if (
            request.user.groups.filter(name="accountant").exists()
            and request.user.is_staff
        ):
            return True
        else:
            return False


# store_in_chnage


class isStoreInCharge(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if (
            request.user.groups.filter(name="store_in_charge").exists()
            and request.user.is_staff
        ):
            return True
        else:
            return False


# hr
class isHR(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name="hr").exists() and request.user.is_staff:
            return True
        else:
            return False


# procurement_group = "procurement"
class isProcurementManager(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if (
            request.user.groups.filter(name="procurement_manager").exists()
            and request.user.is_staff
        ):
            return True
        else:
            return False


class isHunter(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name="hunter").exists() and request.user.is_staff:
            return True
        else:
            return False
