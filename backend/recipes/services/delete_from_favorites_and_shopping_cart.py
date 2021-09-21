from django.utils.translation import gettext as _
from rest_framework.serializers import ValidationError


class DoesNotExistError(ValidationError):
    pass


class BaseDeleteService:
    def __init__(self, model, user, recipe):
        self._model = model
        self._user = user
        self._recipe = recipe

    def __call__(self, *args, **kwargs):
        self.valid_data()
        self._delete()

    def valid_data(self):
        obj = self._model.objects.filter(
            user=self._user,
            recipe=self._recipe,
        ).first()
        if obj is None:
            raise DoesNotExistError(
                {'errors': _(f'{self._model.__name__}Object does not exist')},
            )

        return True

    def _delete(self):
        self._model.objects.get(user=self._user, recipe=self._recipe).delete()


class DeleteFromFavorites(BaseDeleteService):
    pass


class DeleteFromShoppingCart(BaseDeleteService):
    pass
