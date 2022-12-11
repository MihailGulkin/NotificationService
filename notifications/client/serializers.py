from rest_framework import serializers
from .models import Tag, Client


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    tag_list = TagSerializer(many=True, read_only=True, source='tag')

    class Meta:
        model = Client
        fields = (
            'pk',
            'phone_number',
            'operator_code',
            'timezone',
            'tag_list',
        )
