from django.urls import include, path
from ingredients.views import IngredientViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls)),
]
