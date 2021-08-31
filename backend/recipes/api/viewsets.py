import io

from config.permissions import IsAuthor
from config.settings import SITE_ROOT
from config.viewsets import AppViewSet, MultiPermissionMixin
from django.db.models import Sum
from django.http import FileResponse
from ingredients.models import RecipeIngredient
from recipes.api import serializers
from recipes.filters import RecipeFilter
from recipes.models import Favorite, Recipe, ShoppingCart
from recipes.services.add_to_favorites_and_shopping_cart import (
    AddToFavorites,
    AddToShoppingCart,
)
from recipes.services.delete_from_favorites_and_shopping_cart import (
    DeleteFromFavorites,
    DeleteFromShoppingCart,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class RecipeViewSet(MultiPermissionMixin, AppViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    filterset_class = RecipeFilter
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
    favorite_method_services = {
        'get': lambda self, **kwargs: self.add_to_favorites(**kwargs),
        'delete': lambda self, **kwargs: self.delete_from_favorites(**kwargs),
    }
    shopping_cart_method_services = {
        'get': lambda self, **kwargs: self.add_to_shopping_cart(**kwargs),
        'delete': lambda self, **kwargs: self.delete_from_shopping_cart(**kwargs),
    }

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()

        representation = self.serializer_class(
            recipe,
            context={'request': request},
        ).data
        return Response(representation, status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()

        representation = self.serializer_class(
            recipe,
            context={'request': request},
        ).data
        return Response(representation, status=status.HTTP_200_OK)

    @action(methods=['get', 'delete'], detail=True)
    def favorite(self, request, **kwargs):
        method = request.method.lower()
        return self.favorite_method_services[method](
            self=self,
            request=request,
            pk=kwargs.get('pk'),
        )

    @action(methods=['get', 'delete'], detail=True)
    def shopping_cart(self, request, **kwargs):
        method = request.method.lower()
        return self.shopping_cart_method_services[method](
            self=self,
            request=request,
            pk=kwargs.get('pk'),
        )

    def _get_service_args(self, **kwargs):
        user = kwargs.get('request').user
        recipe = self.get_object()
        return user, recipe

    def get_action_method(self, **kwargs):
        service, model, request, pk = kwargs.values()
        user, recipe = self._get_service_args(request=request)
        data = {'user': user.id, 'recipe': pk}

        serializer = self.get_serializer_class()(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        service(model=model, user=user, recipe=recipe)()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_action_method(self, **kwargs):
        service, model, request, _ = kwargs.values()
        user, recipe = self._get_service_args(request=request)

        service(model=model, user=user, recipe=recipe)()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def add_to_favorites(self, **kwargs):
        return self.get_action_method(service=AddToFavorites, model=Favorite, **kwargs)

    def add_to_shopping_cart(self, **kwargs):
        return self.get_action_method(service=AddToShoppingCart, model=ShoppingCart, **kwargs)

    def delete_from_favorites(self, **kwargs):
        return self.delete_action_method(service=DeleteFromFavorites, model=Favorite, **kwargs)

    def delete_from_shopping_cart(self, **kwargs):
        return self.delete_action_method(service=DeleteFromShoppingCart, model=ShoppingCart, **kwargs)

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
