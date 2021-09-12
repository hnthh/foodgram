import io

from config.settings import SITE_ROOT
from django.db.models import Sum
from recipes.models import RecipeIngredient
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONTS_ROOT = f'{SITE_ROOT}/staticfiles/fonts'


class ShoppingCartPDFCreator:
    def __init__(self, user, font):
        self._user = user
        self._font = font

        self._path = self._get_path()
        self._purchases = self._get_queryset()

    def __call__(self, *args, **kwargs):
        self._register_font()

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)

        purchases = pdf.beginText(0, 650)
        purchases.setFont(self._font, 15)

        for number, ingredient in enumerate(self._purchases, start=1):
            name, unit, total = ingredient.values()
            purchases.textLine(f'{number}) {name} — {total} ({unit})')

        pdf.drawText(purchases)
        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        return buffer

    def _get_path(self):
        return f'{FONTS_ROOT}/{self._font}.ttf'

    def _register_font(self):
        pdfmetrics.registerFont(
            TTFont(self._font, self._path),
        )

    def _get_queryset(self):
        return RecipeIngredient.objects.filter(
            recipe__purchases__user=self._user,
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(
            total=Sum('amount'),
        )
