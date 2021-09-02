from config.serializers import DoMixin, ModelSerializer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer,
)
from djoser.serializers import UserSerializer as DjoserUserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscribe

User = get_user_model()


class UserSerializer(DoMixin, DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return Subscribe.objects.filter(user=user, author=author).exists()


class UserCreateSerializer(DjoserUserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class SubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, user):
        from recipes.api.serializers import RecipeSubscriptionSerializer

        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit',
        )
        queryset = Recipe.objects.filter(author=user)
        if recipes_limit is not None:
            queryset = queryset[:int(recipes_limit)]

        return RecipeSubscriptionSerializer(queryset, many=True).data

    def get_recipes_count(self, user):
        return user.recipes.count()


class SubscribeSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscribe
        fields = ('user', 'author')
        validators = (
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('user', 'author'),
                message='Subscription already exists',
            ),
        )

    def validate(self, data):
        if data['user'] == data['author']:
            raise serializers.ValidationError(_('You cannot subscribe to yourself'))
        return data


class UnsubscribeSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscribe
        fields = ('user', 'author')

    def validate(self, data):
        user, author = data.values()

        subscription = Subscribe.objects.filter(user=user, author=author).first()
        if subscription is None:
            raise serializers.ValidationError(_('Subscription does not exist'))
        return data
