from django.urls import include, path
from recipes.api.viewsets import RecipeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
]
