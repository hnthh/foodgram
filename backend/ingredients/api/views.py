from ingredients.api.serializers import IngredientSerializer
from ingredients.filters import IngredientFilter
from ingredients.models import Ingredient
from rest_framework.viewsets import ReadOnlyModelViewSet


class IngredientViewSet(ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None
