from django.urls import include, path
from ingredients.api.viewsets import IngredientViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls)),
]
