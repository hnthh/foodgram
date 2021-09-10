from rest_framework import serializers


class Do:  # noqa: PIE798
    @classmethod
    def do(cls, data, context=None):
        instance = cls(data=data, context=context)

        return instance.is_valid(raise_exception=True)


class ModelSerializer(Do, serializers.ModelSerializer):

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            try:
                fields = fields + self.Meta.extra_fields
            except TypeError:
                fields = fields + type(fields)(self.Meta.extra_fields)

        return fields
