from rest_framework import permissions
from django.contrib.auth.models import User


class IsValidLogin(permissions.BasePermission):
    """
    Custom permission to only allow clients who are the owner of the object.
    """

    def has_permission(self, request, *args, **kwargs):

        try:
            user = User.objects.get(id=request.user.id)
            if user.is_active:
                return True
            else:
                return False
        except User.DoesNotExist:
            return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, *args, **kwargs):
        if (
            request.user.is_staff
            and request.user.groups.filter(name="admins").exists()
            and request.user.groups.filter(name="directors").exists()
        ):
            return True
        elif (
            request.user.is_staff and request.user.groups.filter(name="admins").exists()
        ):
            return True
        elif (
            request.user.is_staff
            and request.user.groups.filter(name="directors").exists()
        ):
            return True
        else:
            return False


class IsDirector(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, *args, **kwargs):
        if (
            request.user.is_staff
            and request.user.groups.filter(name="directors").exists()
        ):
            return True
        else:
            return False


class IsOwnerOrAdminOrAccountant(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, *args, **kwargs):
        if (
            request.user.is_staff
            and request.user.groups.filter(name="admins").exists()
            and request.user.groups.filter(name="directors").exists()
        ):
            return True
        elif (
            request.user.is_staff and request.user.groups.filter(name="admins").exists()
        ):
            return True
        elif (
            request.user.is_staff
            and request.user.groups.filter(name="directors").exists()
        ):
            return True
        elif (
            request.user.is_staff
            and request.user.groups.filter(name="accountants").exists()
        ):
            return True
        else:
            return False


class IsOwnerOrAdminOrDirectorOrOperator(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, *args, **kwargs):
        if (
            request.user.is_staff
            and request.user.groups.filter(name="admins").exists()
            and request.user.groups.filter(name="directors").exists()
            and request.user.groups.filter(name="operators").exists()
        ):
            return True
        elif (
            request.user.is_staff
            and request.user.groups.filter(name="admins").exists()
            and request.user.groups.filter(name="directors").exists()
        ):
            return True
        elif (
            request.user.is_staff
            and request.user.groups.filter(name="admins").exists()
            and request.user.groups.filter(name="operators").exists()
        ):
            return True
        elif (
            request.user.is_staff
            and request.user.groups.filter(name="directors").exists()
            and request.user.groups.filter(name="operators").exists()
        ):
            return True
        elif (
            request.user.is_staff and request.user.groups.filter(name="admins").exists()
        ):
            return True
        elif (
            request.user.is_staff
            and request.user.groups.filter(name="directors").exists()
        ):
            return True
        elif (
            request.user.is_staff
            and request.user.groups.filter(name="operators").exists()
        ):
            return True
        else:
            return False


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, *args, **kwargs):
        if request.user.groups.filter(name="admins").exists() and request.user.is_staff:
            return True
        else:
            return False


class IsOperator(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, *args, **kwargs):
        if (
            request.user.groups.filter(name="operators").exists()
            and request.user.is_staff
        ):
            return True
        else:
            return False


# accountant
class IsAccountant(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, *args, **kwargs):
        if (
            request.user.groups.filter(name="accountants").exists()
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

    def has_permission(self, request, *args, **kwargs):
        if (
            request.user.groups.filter(name="store_in_chargers").exists()
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

    def has_permission(self, request, *args, **kwargs):
        if request.user.groups.filter(name="hrs").exists() and request.user.is_staff:
            return True
        else:
            return False


# procurement_group = "procurement"
class isProcurementManager(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, *args, **kwargs):
        if (
            request.user.groups.filter(name="procurement_managers").exists()
            and request.user.is_staff
        ):
            return True
        else:
            return False


class isClient(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, *args, **kwargs):
        if (
            request.user.groups.filter(name="clients").exists()
            and request.user.is_staff
        ):
            return True
        else:
            return False
