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
    is_subscribed = serializers.BooleanField(read_only=True)

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

    def to_representation(self, user):
        request = self.context['request']

        qs = self.Meta.model.objects.for_detail(user.pk, request.user)

        return super().to_representation(qs)


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
        extra_kwargs = {'password': {'write_only': True}}


class SubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)

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

    def get_recipes(self, author):
        from recipes.api.serializers import RecipeSubscriptionSerializer

        limit = self.context['request'].query_params.get('recipes_limit')

        qs = (
            Recipe.objects.for_author(author)[:int(limit)]
            if limit is not None
            else Recipe.objects.for_author(author)
        )

        return RecipeSubscriptionSerializer(qs, many=True).data


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

    def create(self, data):
        user, author = data.values()
        return user.subscribe(author)

    def to_representation(self, subscription):
        from users.api.serializers import SubscriptionSerializer

        qs = User.objects.for_detail(subscription.author.id, subscription.user)
        return SubscriptionSerializer(qs, context=self.context).data


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
