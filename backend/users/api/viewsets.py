from config.viewsets import MultiSerializerMixin
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from users.api import serializers
from users.services.subscriber import Subscriber
from users.services.unsubscriber import Unsubscriber

User = get_user_model()


class UserViewSet(MultiSerializerMixin, DjoserUserViewSet):
    serializer_action_classes = {
        'subscribe': serializers.SubscribeSerializer,
        'subscriptions': serializers.SubscriptionSerializer,
    }
    subscribe_method_dispatcher = {
        'get': lambda self, *args: self._subscribe(Subscriber, *args),
        'delete': lambda self, *args: self._unsubscribe(Unsubscriber, *args),
    }

    def destroy(self, request, **kwargs):
        raise MethodNotAllowed(request.method)

    def update(self, request, **kwargs):
        raise MethodNotAllowed(request.method)

    @action(methods=['get', 'delete'], detail=True)
    def subscribe(self, request, id):
        method = request.method.lower()
        return self.subscribe_method_dispatcher[method](self, request, id)

    def _subscribe(self, *args):
        service, request, pk = args
        author = User.objects.get(pk=pk)

        data = {'user': request.user.id, 'author': pk}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        service(user=request.user, author=author)()

        representation = self.get_serializer_class(action='subscriptions')(
            author,
            context={'request': request},
        )
        return Response(representation.data, status=status.HTTP_201_CREATED)

    def _unsubscribe(self, *args):
        service, request, pk = args
        author = User.objects.get(pk=pk)

        service(user=request.user, author=author)()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def subscriptions(self, request):
        return self.list(request)

    def get_queryset(self):
        if self.action == 'subscriptions':
            return User.objects.filter(
                following__user=self.request.user,
            )
        return self.queryset
