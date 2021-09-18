from config.serializers import ModelSerializer, serializers
from drf_extra_fields.fields import Base64ImageField
from ingredients.models import Ingredient
from recipes.models import Favorite, Recipe, RecipeIngredient, ShoppingCart
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from tags.api.serializers import TagSerializer
from tags.models import Tag
from users.api.serializers import UserSerializer


class RecipeIngredientSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all(),
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredients')
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ('created', 'modified')
        extra_fields = ('is_favorited', 'is_in_shopping_cart')


class RecipeSubscriptionSerializer(RecipeSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeCreateSerializer(ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def to_representation(self, recipe):
        request = self.context['request']

        qs = self.Meta.model.objects.for_detail(recipe.pk, request.user)

        return RecipeSerializer(qs, context=self.context).data

    def create(self, data):
        return Recipe.objects.create_with_ingredients_and_tags(**data)


class RecipeUpdateSerializer(ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'image', 'cooking_time', 'ingredients', 'tags')
        extra_kwargs = {
            'name': {'required': False},
            'text': {'required': False},
            'cooking_time': {'required': False},
        }

    def to_representation(self, recipe):
        request = self.context['request']

        qs = self.Meta.model.objects.for_detail(recipe.pk, request.user)

        return RecipeSerializer(qs, context=self.context).data

    def update(self, recipe, data):
        return recipe.update(**data)


class FavoriteBaseSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=True)
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all(), write_only=True)

    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')
    image = Base64ImageField(source='recipe.image', read_only=True)

    class Meta:
        model = Favorite
        exclude = ('created', 'modified')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='FavoriteObject already exists',
            ),
        ]


class FavoriteSerializer(FavoriteBaseSerializer):
    pass


class ShoppingCartSerializer(FavoriteBaseSerializer):

    class Meta(FavoriteBaseSerializer.Meta):
        model = ShoppingCart
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='ShoppingCartObject already exists',
            ),
        ]
