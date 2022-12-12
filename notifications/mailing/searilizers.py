from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field

from .mixins import SerializerValidate
from .models import (
    Mailing,
    Message,
    Filter,
)


class FilterSerializer(
    SerializerValidate,
    serializers.ModelSerializer,
):
    class Meta:
        model = Filter
        fields = '__all__'

    def validate(self, data):
        return self._validate(data, Filter)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MailingSerializer(
    SerializerValidate,
    serializers.ModelSerializer
):

    msg_group_by_status = serializers.SerializerMethodField()
    count_msg = serializers.SerializerMethodField()

    class Meta:
        model = Mailing
        fields = (
            'pk',
            'start_mailing_time',
            'message_text',
            'client_filter',
            'end_mailing_time',
            'created_at',
            'count_msg',
            'msg_group_by_status',
        )

    @extend_schema_field(
        {'type': "dict", 'format': 'json',
         'example': {
             "200": [
                 {
                     "id": 1,
                     "mailing_send": "2022-12-10T08:14:53.142Z",
                     "mailing_status": 200,
                     "mailing_id": 1,
                     "client_id": 1
                 }
             ],
         }
         })
    def get_msg_group_by_status(self, obj) -> \
            dict[Message.mailing_status, list[Message]]:
        queryset = Message.objects.filter(mailing_id_id=obj.pk)
        _dict = {}
        for msg in queryset:
            serialized = MessageSerializer(msg).data
            if msg.mailing_status in _dict:
                _dict[msg.mailing_status].append(serialized)
            else:
                _dict.setdefault(msg.mailing_status, [serialized])
        return _dict

    def get_count_msg(self, obj) -> int:
        return len(Message.objects.filter(mailing_id_id=obj.pk))

    def validate(self, data):
        return self._validate(data, Mailing)
