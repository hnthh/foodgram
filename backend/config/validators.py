from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class GtMinValueValidator(MinValueValidator):
    message = _('Ensure this value is greater than %(limit_value)s.')
    code = 'min_value'

    def compare(self, a, b):
        return a <= b
