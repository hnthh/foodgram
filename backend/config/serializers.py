from rest_framework.serializers import ModelSerializer as _ModelSerializer


class DoMixin:
    @classmethod
    def do(self, data, context=None):
        instance = self(data=data, context=context)

        return instance.is_valid(raise_exception=True)


class ModelSerializer(DoMixin, _ModelSerializer):
    pass
