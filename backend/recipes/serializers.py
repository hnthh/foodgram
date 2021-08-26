from drf_extra_fields.fields import Base64ImageField
from recipes.decorators import recipe_create_update
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class AddIngredientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
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
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
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

    def get_ingredients(self, recipe):
        queryset = RecipeIngredient.objects.filter(recipe=recipe)
        return RecipeIngredientSerializer(queryset, many=True).data

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return Favorite.objects.filter(user=user, recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=recipe).exists()


class RecipeSubscriptionSerializer(RecipeSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = AddIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def to_representation(self, recipe):
        return RecipeSerializer(
            recipe,
            context={'request': self.context['request']},
        ).data

    @recipe_create_update
    def create(self, validated_data):
        return Recipe.objects.create(**validated_data)

    @recipe_create_update
    def update(self, recipe, validated_data):
        recipe.recipeingredient_set.all().delete()
        recipe.tags.remove()

        Recipe.objects.filter(id=recipe.id).update(**validated_data)
        recipe.refresh_from_db()
        return recipe


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

    def get_image(self, favorite):
        request = self.context.get('request')
        image_url = favorite.recipe.image.url
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

    def get_image(self, shopping_cart):
        request = self.context.get('request')
        image_url = shopping_cart.recipe.image.url
        return request.build_absolute_uri(image_url)
