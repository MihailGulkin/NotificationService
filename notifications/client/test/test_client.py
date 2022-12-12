from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from client.models import Client
from client.serializers import ClientSerializer


class ClientTestCase(APITestCase):
    """
    Test Cases for :model:`client.Client`.
    """
    all_client_url = reverse('all-client')
    create_client_url = reverse('create-client')

    def setUp(self) -> None:
        self.client_1 = Client.objects.create(
            phone_number=79102223344,
            operator_code=910,
            timezone='Europe/Moscow'
        )
        self.client_2 = Client.objects.create(
            phone_number=79102223355,
            operator_code=910,
            timezone='Europe/Moscow'
        )

    def test_all_client(self):
        """
        Test GET all-client endpoint.
        """
        response = self.client.get(self.all_client_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        resp_json = response.json()['results']

        self.assertEqual(
            resp_json[0],
            ClientSerializer(self.client_1).data
        )
        self.assertEqual(
            resp_json[1],
            ClientSerializer(self.client_2).data
        )

    def test_create_client(self):
        """
        Test POST create client endpoint.
        """
        json = {
            'phone_number': '79102223366',
            'operator_code': 910,
            'timezone': 'Europe/Moscow'
        }
        response = self.client.post(
            self.create_client_url,
            data=json,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        resp_json = response.json()
        self.assertEqual(
            Client.objects.get(pk=resp_json.get('pk')).phone_number,
            resp_json.get('phone_number')
        )

    def test_delete_client(self):
        """
        Test DELETE client endpoint
        """
        client_pk = self.client_1.pk
        delete_client_url = reverse('destroy-client', args=[client_pk])

        response = self.client.delete(delete_client_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            0,
            len(Client.objects.filter(pk=client_pk))
        )

    def test_update_put_client(self):
        """
        Test PUT client endpoint.
        """
        client_pk = self.client_1.pk
        update_client_url = reverse('update-client', args=[client_pk])
        json = {
            'phone_number': '79162223377',
            'operator_code': 916,
            'timezone': 'Europe/Moscow'
        }

        response = self.client.put(update_client_url, data=json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        res_json = response.json()
        upd_client = Client.objects.get(pk=client_pk)

        self.assertNotEqual(
            ClientSerializer(res_json).data,
            self.client_1
        )
        self.assertEqual(
            json.get('operator_code'),
            upd_client.operator_code
        )
        self.assertEqual(
            json.get('phone_number'),
            upd_client.phone_number
        )

    def test_update_patch_client(self):
        """
        Test PATCH client endpoint.
        """
        client_pk = self.client_1.pk
        update_client_url = reverse('update-client', args=[client_pk])
        json = {
            'timezone': 'America/Araguaina',
        }

        response = self.client.patch(update_client_url, data=json)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        res_json = response.json()

        self.assertNotEqual(
            ClientSerializer(res_json).data,
            self.client_1
        )
        self.assertEqual(
            self.client_1.operator_code,
            res_json.get('operator_code')
        )
        self.assertEqual(
            self.client_1.phone_number,
            int(res_json.get('phone_number')),
        )
