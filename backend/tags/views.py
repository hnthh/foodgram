from rest_framework.viewsets import ReadOnlyModelViewSet
from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
