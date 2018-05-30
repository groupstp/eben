from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow Author of an object.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsDoer(permissions.BasePermission):
    """
    Custom permission to only allow doers of an object.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.doer == request.user
