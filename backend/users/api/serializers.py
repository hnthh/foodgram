from config.serializers import ModelSerializer, serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer,
)
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscribe

User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_subscribed')

    def to_representation(self, user):
        request = self.context['request']

        qs = self.Meta.model.objects.for_detail(user.pk, request.user)

        return super().to_representation(qs)


class UserCreateSerializer(DjoserUserCreateSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')


class SubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, author):
        from recipes.api.serializers import RecipeSubscriptionSerializer

        limit = self.context['request'].query_params.get('recipes_limit')

        qs = (
            author.recipes.all()[:int(limit)]
            if limit is not None
            else author.recipes.all()
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
        if not Subscribe.objects.filter(**data).exists():
            raise serializers.ValidationError(_('Subscription does not exist'))
        return data
