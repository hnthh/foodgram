import io

from config.permissions import IsAuthor
from config.settings import SITE_ROOT
from config.viewsets import AppViewSet, MultiPermissionMixin
from django.db.models import Sum
from django.http import FileResponse
from ingredients.models import RecipeIngredient
from recipes.api import serializers
from recipes.decorators import recipe_favorite_shoppingcart_actions
from recipes.filters import RecipeFilter
from recipes.models import Favorite, Recipe, ShoppingCart
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class RecipeViewSet(MultiPermissionMixin, AppViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    serializer_action_classes = {
        'create': serializers.RecipeCreateUpdateSerializer,
        'update': serializers.RecipeCreateUpdateSerializer,
        'favorite': serializers.FavoriteSerializer,
        'shopping_cart': serializers.ShoppingCartSerializer,
    }
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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()

        representation = self.serializer_class(
            recipe,
            context={'request': request},
        ).data
        return Response(representation, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()

        representation = self.serializer_class(
            recipe,
            context={'request': request},
        ).data
        return Response(representation, status=status.HTTP_200_OK)

    @action(
        methods=['get', 'delete'],
        detail=True,
    )
    @recipe_favorite_shoppingcart_actions
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        Favorite.objects.get(user=request.user, recipe=recipe).delete()

    @action(
        methods=['get', 'delete'],
        detail=True,
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
            f'{SITE_ROOT}/staticfiles/fonts/'
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
