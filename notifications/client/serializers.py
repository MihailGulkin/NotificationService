from rest_framework import serializers
from .models import Tag, Client


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    tag_list = TagSerializer(many=True, source='tag')

    def update(self, instance, validated_data):
        tag = Tag.objects.filter(tag_name=validated_data['tag'][0]['tag_name']).first()
        instance.tag.add(tag)
        return instance

    class Meta:
        model = Client
        fields = (
            'pk',
            'phone_number',
            'operator_code',
            'timezone',
            'tag_list',
        )
