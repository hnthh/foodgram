from config.testing import register


@register
def tag(self, **kwargs):
    return self.mixer.blend(
        'tags.Tag',
        name='Завтрак',
        color='#FFB500',
        slug='breakfast',
        **kwargs,
    )


@register
def tags(self, **kwargs):
    return self.mixer.cycle(3).blend(
        'tags.Tag', name=(
            name for name in ('Завтрак', 'Обед', 'Ужин')
        ), color=(
            color for color in ('#FFB500', '#F93800', '#283350')
        ), slug=(
            slug for slug in ('breakfast', 'lunch', 'dinner')
        ),
        **kwargs,
    )
