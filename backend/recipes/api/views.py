import io

from config.mixins import MultiPermissionViewSetMixin
from config.permissions import IsAuthor
from config.settings import SITE_ROOT
from django.db.models import Sum
from django.http import FileResponse
from ingredients.models import RecipeIngredient
from recipes.api.serializers import (
    FavoriteSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
)
from recipes.decorators import recipe_favorite_shoppingcart_actions
from recipes.filters import RecipeFilter
from recipes.models import Favorite, Recipe, ShoppingCart
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class RecipeViewSet(MultiPermissionViewSetMixin, ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = {
        'list': (AllowAny,),
        'create': (IsAuthenticated,),
        'retrieve': (AllowAny,),
        'update': (IsAuthor,),
        'destroy': (IsAuthor,),
        'favorite': (IsAuthenticated,),
        'shopping_cart': (IsAuthenticated,),
        'download_shopping_cart': (IsAuthenticated,),
    }
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return RecipeCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['get', 'delete'],
        detail=True,
        serializer_class=FavoriteSerializer,
    )
    @recipe_favorite_shoppingcart_actions
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        Favorite.objects.get(user=request.user, recipe=recipe).delete()

    @action(
        methods=['get', 'delete'],
        detail=True,
        serializer_class=ShoppingCartSerializer,
    )
    @recipe_favorite_shoppingcart_actions
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        return ShoppingCart.objects.get(
            user=request.user, recipe=recipe,
        ).delete()

    @action(detail=False)
    def download_shopping_cart(self, request):
        path = (
            f'{SITE_ROOT}/static/fonts/'
            'IBMPlexMono-ExtraLightItalic.ttf'
        )
        pdfmetrics.registerFont(
            TTFont('IBMPlexMono-ExtraLightItalic', path),
        )

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)

        purchases = pdf.beginText(0, 650)
        purchases.setFont('IBMPlexMono-ExtraLightItalic', 15)

        ingredients = RecipeIngredient.objects.filter(
            recipe__purchases__user=request.user,
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(
            total=Sum('amount'),
        )

        for number, ingredient in enumerate(ingredients, start=1):
            name, unit, total = ingredient.values()
            purchases.textLine(f'{number}) {name} — {total} ({unit})')

        pdf.drawText(purchases)
        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='ingredients.pdf',
        )
