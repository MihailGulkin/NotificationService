from rest_framework import serializers


class SerializerValidate:
    """
    Mixin for reuse validate method in serializer
    """
    def _validate(self, data, model):

        instance = model(**data)
        try:
            instance.clean()
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.args[0])

        return data
