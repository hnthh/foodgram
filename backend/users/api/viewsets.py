from config.viewsets import AppUserViewSet
from django.contrib.auth import get_user_model
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


class UserViewSet(AppUserViewSet):
    subscribe_method_dispatcher = {
        'get': lambda self, request, pk: self._subscribe(request, pk),
        'delete': lambda self, request, pk: self._unsubscribe(request, pk),
    }

    def destroy(self, request, **kwargs):
        raise MethodNotAllowed(request.method)

    def update(self, request, **kwargs):
        raise MethodNotAllowed(request.method)

    def get_queryset(self):
        qs = User.objects.for_subscriptions(self.request.user)

        if self.action != 'subscriptions':
            qs = User.objects.for_viewset(self.request.user)

        return qs

    @action(methods=['get', 'delete'], detail=True)
    def subscribe(self, request, id):
        method = request.method.lower()
        return self.subscribe_method_dispatcher[method](self, request, id)

    def _subscribe(self, request, pk):
        context = self.get_serializer_context()
        serializer = SubscribeSerializer(data={'author': pk}, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _unsubscribe(self, request, pk):
        context = self.get_serializer_context()
        author = User.objects.get(pk=pk)

        UnsubscribeSerializer.do(data={'author': pk}, context=context)
        request.user.unsubscribe(author)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, serializer_class=SubscriptionSerializer)
    def subscriptions(self, request):
        return self.list(request)
