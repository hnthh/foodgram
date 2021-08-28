from config.testing import register


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
