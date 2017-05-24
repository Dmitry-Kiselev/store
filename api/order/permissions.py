from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user

        elif hasattr(obj, 'basket'):
            return obj.basket.user == request.user
