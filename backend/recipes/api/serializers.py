from drf_extra_fields.fields import Base64ImageField
from ingredients.models import Ingredient, RecipeIngredient
from recipes.models import Favorite, Recipe, ShoppingCart
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from tags.api.serializers import TagSerializer
from tags.models import Tag
from users.api.serializers import UserSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all(),
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipeingredient_set',
    )
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class RecipeSubscriptionSerializer(RecipeSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = (
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def to_representation(self, recipe):
        request, *_, action = self.context.values()

        qs = Recipe.objects.for_viewset(request.user)
        if action != 'retrieve':
            qs = Recipe.objects.for_detail(recipe.id, request.user)

        return RecipeSerializer(qs, context={'request': request}).data

    def create(self, data):
        return Recipe.objects.create_with_ingredients_and_tags(**data)

    def update(self, recipe, data):
        return recipe.update(**data)


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
            'user',
            'recipe',
        )
        extra_kwargs = {
            'user': {'write_only': True},
            'recipe': {'write_only': True},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='FavoriteObject already exists',
            ),
        ]

    def get_image(self, ordered):
        _, recipe = ordered.values()
        request = self.context.get('request')
        image_url = recipe.image.url
        return request.build_absolute_uri(image_url)


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')
    image = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
            'user',
            'recipe',
        )
        extra_kwargs = {
            'user': {'write_only': True},
            'recipe': {'write_only': True},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='ShoppingCartObject already exists',
            ),
        ]

    def get_image(self, ordered):
        _, recipe = ordered.values()
        request = self.context.get('request')
        image_url = recipe.image.url
        return request.build_absolute_uri(image_url)
