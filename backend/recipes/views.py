import io

from config.mixins import MultiPermissionViewSetMixin
from config.permissions import IsAuthor
from config.settings import SITE_ROOT
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from recipes.serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class IngredientViewSet(ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter

    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


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
    filter_backends = (DjangoFilterBackend,)
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
    def favorite(self, request, pk):
        user = request.user
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, pk=pk)
            try:
                Favorite.objects.get(user=user, recipe=recipe).delete()
            except ObjectDoesNotExist:
                return Response(
                    {'errors': 'FavoriteObject does not exist'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

        data = {'user': user.pk, 'recipe': pk}
        serializer = self.get_serializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['get', 'delete'],
        detail=True,
        serializer_class=ShoppingCartSerializer,
    )
    def shopping_cart(self, request, pk):
        user = request.user
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, pk=pk)
            try:
                ShoppingCart.objects.get(user=user, recipe=recipe).delete()
            except ObjectDoesNotExist:
                return Response(
                    {'errors': 'ShoppingCartObject does not exist'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

        data = {'user': user.pk, 'recipe': pk}
        serializer = self.get_serializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
