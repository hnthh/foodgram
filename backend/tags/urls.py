from django.urls import include, path
from rest_framework.routers import DefaultRouter
from tags.api.views import TagViewSet

router = DefaultRouter()
router.register('', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]
