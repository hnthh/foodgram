from collections.abc import Iterable

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

__all__ = [
    'AppUserViewSet',
    'AppViewSet',
    'ReadOnlyAppViewSet',
]


class MultiSerializerMixin:
    def get_serializer_class(self, action=None):
        if action is None:
            action = self.action

        try:
            return self.serializer_action_classes[action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class MultiPermissionMixin:
    def get_permissions(self):
        try:
            permissions = self.permission_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_permissions()

        if not isinstance(permissions, Iterable):
            converter = list()
            converter.append(permissions)
            permissions = converter

        return (permission() for permission in permissions)


class SerializerUpdatedContextMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'action': self.action})
        return context


class ReadOnlyAppViewSet(MultiSerializerMixin, MultiPermissionMixin, ReadOnlyModelViewSet):
    pass


class AppUserViewSet(SerializerUpdatedContextMixin, DjoserUserViewSet):
    pass


class AppViewSet(
    MultiSerializerMixin,
    MultiPermissionMixin,
    SerializerUpdatedContextMixin,
    ModelViewSet,
):
    pass
