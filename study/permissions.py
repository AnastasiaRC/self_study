from rest_framework.permissions import BasePermission
from users.models import UserRoles


class IsAdmin(BasePermission):
    message = "Вы не модератор!"

    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return True
        return False


class IsAuthor(BasePermission):
    message = 'Вы не владелец!'

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False
