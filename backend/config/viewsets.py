from config.permissions import NotGranted
from rest_framework.permissions import AllowAny
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
        action = self.action
        try:
            permissions = self.permission_classes[action]
        except (KeyError, AttributeError):
            if action not in self.get_extra_actions():
                permissions = [AllowAny]
            else:
                permissions = [NotGranted]

        return (permission() for permission in permissions)


class ReadOnlyAppViewSet(MultiSerializerMixin, _ReadOnlyModelViewSet):
    pass


class AppViewSet(MultiSerializerMixin, ModelViewSet):
    pass
