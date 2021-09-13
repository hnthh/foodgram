import matplotlib._color_data as mcd
from config.models import DefaultModel, models
from django.core.validators import RegexValidator

HEX_RE = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'


class Tag(DefaultModel):
    name = models.CharField('название', unique=True, max_length=20)
    color = models.CharField(
        'цвет (HEX)',
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex=HEX_RE,
                message='%(value)s is not a HEX color code.',
            ),
        ],
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'
        default_related_name = 'tags'
        constraints = (
            models.CheckConstraint(
                name='HEX_color',
                check=models.Q(color__regex=HEX_RE),
            ),
        )

    @property
    def color_name(self):
        for name, hex in mcd.XKCD_COLORS.items():
            if self.color.lower() == hex:
                return name.split(':')[1]
        return '—'
