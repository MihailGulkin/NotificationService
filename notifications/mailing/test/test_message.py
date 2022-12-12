from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from client.models import Client
from mailing.models import Mailing, Filter, Message


class MessageTestCase(APITestCase):
    """
    Test Cases for :model:`mailing.Message`
    """

    def setUp(self) -> None:
        self.filter_1 = Filter.objects.create(
            filter_type='Tag',
            filter_value='test'
        )
        self.mailing_1 = Mailing.objects.create(
            start_mailing_time="2023-12-10T17:35:15.608Z",
            end_mailing_time="2023-12-10T17:36:15.608Z",
            message_text='test_1',
            client_filter_id=self.filter_1.pk,
        )

    def test_list_message(self):
        """
        Test GET list-message-mailing_pk endpoint.
        """
        mailing_pk = self.mailing_1.pk
        list_message_url = reverse(
            'list-message-mailing_pk',
            args=[mailing_pk]
        )
        client_1 = Client.objects.create(
            phone_number=79102223344,
            operator_code=910,
            timezone='Europe/Moscow'
        )
        message_1 = Message.objects.create(
            mailing_id_id=self.mailing_1.pk,
            mailing_send="2030-12-10T17:35:15.608Z",
            mailing_status=200,
            client_id_id=client_1.pk
        )
        message_2 = Message.objects.create(
            mailing_id_id=self.mailing_1.pk,
            mailing_send="2030-12-10T17:35:15.608Z",
            mailing_status=400,
            client_id_id=client_1.pk
        )
        response = self.client.get(list_message_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        res_json = response.json()['results']

        self.assertEqual(len(res_json), 2)

        self.assertEqual(
            res_json[0]['mailing_status'],
            message_1.mailing_status
        )
        self.assertEqual(
            res_json[1]['mailing_status'],
            message_2.mailing_status
        )
