from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from users.models import Subscribe
from users.serializers import SubscribeSerializer, SubscriptionSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet):

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=['get', 'delete'],
        detail=True,
        serializer_class=SubscribeSerializer,
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'GET':
            data = {'user': user.id, 'author': id}
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            output = SubscriptionSerializer(
                author,
                context={'request': request},
            )
            return Response(output.data, status=status.HTTP_201_CREATED)

        try:
            subscribe = Subscribe.objects.get(user=user, author=author)
        except ObjectDoesNotExist:
            raise ValidationError(
                {'errors': 'Subscribe object does not exist'},
            )

        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        serializer_class=SubscriptionSerializer,
    )
    def subscriptions(self, request):
        return self.list(request)

    def get_queryset(self):
        if self.action == 'subscriptions':
            return User.objects.filter(
                following__user=self.request.user,
            )
        return self.queryset
