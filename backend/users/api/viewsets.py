from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from users.api.serializers import (
    SubscribeSerializer,
    SubscriptionSerializer,
    UnsubscribeSerializer,
)

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    subscribe_method_dispatcher = {
        'get': lambda self, request, pk: self._subscribe(request, pk),
        'delete': lambda self, request, pk: self._unsubscribe(request, pk),
    }

    def destroy(self, request, **kwargs):
        raise MethodNotAllowed(request.method)

    def update(self, request, **kwargs):
        raise MethodNotAllowed(request.method)

    @action(methods=['get', 'delete'], detail=True)
    def subscribe(self, request, id):
        method = request.method.lower()
        return self.subscribe_method_dispatcher[method](self, request, id)

    def _subscribe(self, request, pk):
        author = User.objects.get(pk=pk)

        SubscribeSerializer.do(data={'author': pk}, context={'request': request})
        request.user.subscribe(author)

        representation = SubscriptionSerializer(author, context={'request': request})
        return Response(representation.data, status=status.HTTP_201_CREATED)

    def _unsubscribe(self, request, pk):
        author = User.objects.get(pk=pk)

        UnsubscribeSerializer.do(data={'author': pk}, context={'request': request})
        request.user.unsubscribe(author)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, serializer_class=SubscriptionSerializer)
    def subscriptions(self, request):
        return self.list(request)

    def get_queryset(self):
        if self.action == 'subscriptions':
            return User.objects.filter(
                following__user=self.request.user,
            )
        return self.queryset
