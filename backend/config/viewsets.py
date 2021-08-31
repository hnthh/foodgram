from collections.abc import Iterable

from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import (
    ReadOnlyModelViewSet as _ReadOnlyModelViewSet,
)

__all__ = [
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


class ReadOnlyAppViewSet(MultiSerializerMixin, MultiPermissionMixin, _ReadOnlyModelViewSet):
    pass


class AppViewSet(MultiSerializerMixin, MultiPermissionMixin, ModelViewSet):
    pass
