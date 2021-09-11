from config.models import DefaultModel, models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

HEX_RE = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'


class Tag(DefaultModel):
    name = models.CharField(_('tag name'), unique=True, max_length=20)
    color = models.CharField(
        _('tag color'),
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex=HEX_RE,
                message='%(value)s is not a HEX color code.',
            ),
        ],
    )
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        default_related_name = 'tags'
        constraints = (
            models.CheckConstraint(
                name='HEX_color',
                check=models.Q(color__regex=HEX_RE),
            ),
        )
