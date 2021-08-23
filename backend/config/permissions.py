from rest_framework.permissions import BasePermission


class NotGranted(BasePermission):

    def has_permission(self, request, view):
        return False


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user
