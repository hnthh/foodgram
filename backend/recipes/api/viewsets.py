from config.permissions import IsAuthor
from config.viewsets import AppViewSet
from django.http import FileResponse
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
from recipes.services.shopping_cart_pdf_creator import ShoppingCartPDFCreator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class RecipeViewSet(AppViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    serializer_class = serializers.RecipeSerializer
    serializer_action_classes = {
        'create': serializers.RecipeCreateUpdateSerializer,
        'update': serializers.RecipeCreateUpdateSerializer,
        'favorite': serializers.FavoriteSerializer,
        'shopping_cart': serializers.ShoppingCartSerializer,
    }
    permission_action_classes = {
        'list': AllowAny,
        'retrieve': AllowAny,
        'update': IsAuthor,
        'destroy': IsAuthor,
    }
    favorite_method_services = {
        'get': lambda self, **kwargs: self._get_action_method(service=AddToFavorites, **kwargs),
        'delete': lambda self, **kwargs: self._delete_action_method(service=DeleteFromFavorites, **kwargs),
    }
    shopping_cart_method_services = {
        'get': lambda self, **kwargs: self._get_action_method(service=AddToShoppingCart, **kwargs),
        'delete': lambda self, **kwargs: self._delete_action_method(service=DeleteFromShoppingCart, **kwargs),
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
            model=Favorite,
            request=request,
            pk=kwargs.get('pk'),
        )

    @action(methods=['get', 'delete'], detail=True)
    def shopping_cart(self, request, **kwargs):
        method = request.method.lower()
        return self.shopping_cart_method_services[method](
            self=self,
            model=ShoppingCart,
            request=request,
            pk=kwargs.get('pk'),
        )

    def _get_service_args(self, **kwargs):
        user = kwargs.get('request').user
        recipe = self.get_object()
        return user, recipe

    def _get_action_method(self, **kwargs):
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

    def _delete_action_method(self, **kwargs):
        service, model, request, _ = kwargs.values()
        user, recipe = self._get_service_args(request=request)

        service(model=model, user=user, recipe=recipe)()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def download_shopping_cart(self, request):
        buffer = ShoppingCartPDFCreator(user=request.user, font='IBMPlexMono-ExtraLightItalic')()

        return FileResponse(
            buffer,
            as_attachment=True,
            filename='ingredients.pdf',
        )
