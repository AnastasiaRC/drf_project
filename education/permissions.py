from rest_framework import permissions
from users.models import UserRoles


class IsOwner(permissions.BasePermission):
    Message = "Вы не владелец"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return False


class IsModerator(permissions.BasePermission):
    Message = "Вы не модератор"

    def has_permission(self, request, view):
        if request.user == UserRoles.MODERATOR:
            return True
        return False


class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.MEMBER
