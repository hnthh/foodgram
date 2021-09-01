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
from recipes.services.recipe_creator_updater import (
    RecipeCreator,
    RecipeUpdater,
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
    favorite_method_dispatcher = {
        'get': lambda self, *args: self._get_action_method(AddToFavorites, *args),
        'delete': lambda self, *args: self._delete_action_method(DeleteFromFavorites, *args),
    }
    shopping_cart_method_dispatcher = {
        'get': lambda self, *args: self._get_action_method(AddToShoppingCart, *args),
        'delete': lambda self, *args: self._delete_action_method(DeleteFromShoppingCart, *args),
    }

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        creator = RecipeCreator(**serializer.validated_data)()

        representation = self.serializer_class(
            creator,
            context={'request': request},
        ).data
        return Response(representation, status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)

        updater = RecipeUpdater(recipe, **serializer.validated_data)()

        representation = self.serializer_class(
            updater,
            context={'request': request},
        ).data
        return Response(representation, status=status.HTTP_200_OK)

    @action(methods=['get', 'delete'], detail=True)
    def favorite(self, request, pk):
        method = request.method.lower()
        return self.favorite_method_dispatcher[method](
            self, request, pk, Favorite,
        )

    @action(methods=['get', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        method = request.method.lower()
        return self.shopping_cart_method_dispatcher[method](
            self, request, pk, ShoppingCart,
        )

    def _get_action_method(self, *args):
        service, request, pk, model = args
        recipe = self.get_object()
        data = {'user': request.user.id, 'recipe': pk}

        serializer = self.get_serializer_class()(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        service(model=model, user=request.user, recipe=recipe)()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete_action_method(self, *args):
        service, request, pk, model = args
        recipe = self.get_object()

        service(model=model, user=request.user, recipe=recipe)()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def download_shopping_cart(self, request):
        pdf = ShoppingCartPDFCreator(user=request.user, font='IBMPlexMono-ExtraLightItalic')()

        return FileResponse(
            pdf,
            as_attachment=True,
            filename='ingredients.pdf',
        )
