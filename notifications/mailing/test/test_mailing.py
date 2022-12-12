from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from mailing.models import Mailing, Filter


class MailingTestCase(APITestCase):
    """
    Test Cases for :model:`mailing.Mailing`
    """
    all_mailing_url = reverse('list-mailing')
    create_mailing_url = reverse('create-mailing')

    def setUp(self) -> None:
        self.filter_1 = Filter.objects.create(
            filter_type='Tag',
            filter_value='test'
        )
        self.filter_2 = Filter.objects.create(
            filter_type='Operator',
            filter_value='900'
        )
        self.mailing_1 = Mailing.objects.create(
            start_mailing_time="2023-12-10T17:35:15.608Z",
            end_mailing_time="2023-12-10T17:36:15.608Z",
            message_text='test_1',
            client_filter_id=self.filter_1.pk,
        )
        self.mailing_2 = Mailing.objects.create(
            start_mailing_time="2024-12-10T17:35:15.608Z",
            end_mailing_time="2024-12-10T17:36:15.608Z",
            message_text='test_2',
            client_filter_id=self.filter_2.pk,
        )

    def test_all_mailing(self):
        """
        Test GET all-mailing endpoint.
        """
        response = self.client.get(self.all_mailing_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        resp_json = response.json()['results']

        self.assertEqual(
            resp_json[0]['message_text'],
            self.mailing_1.message_text
        )
        self.assertEqual(
            resp_json[1]['message_text'],
            self.mailing_2.message_text
        )

    def test_create_mailing(self):
        """
        Test POST create mailing endpoint.
        """
        json = {
            'start_mailing_time': "2025-12-10T17:35:15.608Z",
            'message_text': 'test_3',
            'client_filter': self.filter_1.pk,
            'end_mailing_time': "2025-12-10T17:36:15.608Z",

        }
        response = self.client.post(
            self.create_mailing_url,
            data=json,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        resp_json = response.json()
        self.assertEqual(
            Mailing.objects.get(pk=resp_json.get('pk')).message_text,
            resp_json.get('message_text')
        )

    def test_delete_mailing(self):
        """
        Test DELETE mailing endpoint.
        """
        mailing_pk = self.mailing_1.pk
        delete_client_url = reverse('destroy-mailing', args=[mailing_pk])

        response = self.client.delete(delete_client_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            0,
            len(Mailing.objects.filter(pk=mailing_pk))
        )

    def test_update_put_mailing(self):
        """
        Test PUT mailing endpoint.
        """
        mailing_pk = self.mailing_2.pk
        update_mailing_url = reverse('update-mailing', args=[mailing_pk])
        json = {
            'start_mailing_time': "2025-12-10T17:35:15.608Z",
            'message_text': 'test_4',
            'client_filter': self.filter_2.pk,
            'end_mailing_time': "2025-12-10T17:36:15.608Z",

        }

        response = self.client.put(update_mailing_url, data=json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        upd_mailing = Mailing.objects.get(pk=mailing_pk)

        self.assertEqual(
            json.get('message_text'),
            upd_mailing.message_text
        )
        self.assertEqual(
            json.get('client_filter'),
            upd_mailing.client_filter_id
        )

    def test_update_patch_mailing(self):
        """
        Test UPDATE mailing endpoint.
        """
        mailing_pk = self.mailing_2.pk
        update_mailing_url = reverse('update-mailing', args=[mailing_pk])
        json = {
            'message_text': 'test_5',
        }

        response = self.client.patch(update_mailing_url, data=json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        upd_mailing = Mailing.objects.get(pk=mailing_pk)
        res_json = response.json()
        self.assertEqual(
            json.get('message_text'),
            upd_mailing.message_text
        )
        self.assertEqual(
            res_json.get('client_filter'),
            self.mailing_2.client_filter_id
        )