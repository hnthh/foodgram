from config.permissions import NotGranted
from rest_framework.permissions import AllowAny


class MultiPermissionViewSetMixin:

    def get_permissions(self):
        action = self.action
        try:
            permissions = self.permission_classes[action]
        except (KeyError, AttributeError):
            if action not in self.get_extra_actions():
                permissions = (AllowAny,)
            else:
                permissions = (NotGranted,)

        return (permission() for permission in permissions)
