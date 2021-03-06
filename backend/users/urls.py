from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from users.api.viewsets import UserViewSet

router = DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
