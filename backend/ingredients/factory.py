from config.testing import register


@register
def ingredient(self, **kwargs):
    return self.mixer.blend('ingredients.Ingredient', **kwargs)


@register
def ingredients(self, **kwargs):
    return self.mixer.cycle(2).blend(
        'ingredients.Ingredient', name=(
            name for name in ('яблочко', 'грушечка')
        ), **kwargs,
    )
