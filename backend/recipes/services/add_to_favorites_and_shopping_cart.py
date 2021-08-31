class BaseAddService:
    def __init__(self, model, user, recipe):
        self._model = model
        self._user = user
        self._recipe = recipe

    def __call__(self, *args, **kwargs):
        return self._factory()

    def _factory(self):
        return self._model.objects.create(
            user=self._user,
            recipe=self._recipe,
        )


class AddToFavorites(BaseAddService):
    pass


class AddToShoppingCart(BaseAddService):
    pass
