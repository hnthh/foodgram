from django.urls import include, path
from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]
