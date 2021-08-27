from config.testing import register


@register
def ingredient(self, **kwargs):
    return self.mixer.blend('recipes.Ingredient', **kwargs)


@register
def ingredients(self, **kwargs):
    return self.mixer.cycle(2).blend(
        'recipes.Ingredient', name=(
            name for name in ('яблочко', 'грушечка')
        ), **kwargs,
    )


@register
def tag(self, **kwargs):
    return self.mixer.blend(
        'recipes.Tag',
        name='Завтрак',
        color='#FFB500',
        slug='breakfast',
        **kwargs,
    )


@register
def tags(self, **kwargs):
    return self.mixer.cycle(3).blend(
        'recipes.Tag', name=(
            name for name in ('Завтрак', 'Обед', 'Ужин')
        ), color=(
            color for color in ('#FFB500', '#F93800', '#283350')
        ), slug=(
            slug for slug in ('breakfast', 'lunch', 'dinner')
        ),
        **kwargs,
    )


@register
def recipe(self, **kwargs):
    return self.mixer.blend(
        'recipes.Recipe',
        **kwargs,
    )


@register
def recipes(self, **kwargs):
    return self.mixer.cycle(2).blend(
        'recipes.Recipe',
        **kwargs,
    )
