from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    message = 'Вы не владелец!'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.pk == request.user.pk