from rest_framework.serializers import ModelSerializer as _ModelSerializer


class Do:  # noqa: PIE798
    @classmethod
    def do(cls, data, context=None):
        instance = cls(data=data, context=context)

        return instance.is_valid(raise_exception=True)


class ModelSerializer(Do, _ModelSerializer):
    pass
