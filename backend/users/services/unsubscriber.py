from django.utils.translation import gettext as _
from rest_framework.serializers import ValidationError
from users.models import Subscribe


class Unsubscriber:
    def __init__(self, user, author):
        self._user = user
        self._author = author

    def __call__(self, *args, **kwargs):
        self.valid_data()
        self._delete()

    def valid_data(self):
        obj = Subscribe.objects.filter(user=self._user, author=self._author).first()
        if obj is None:
            raise ValidationError(
                {'errors': _('Subscribe object does not exist')},
            )

        return True

    def _delete(self):
        Subscribe.objects.get(user=self._user, author=self._author).delete()
