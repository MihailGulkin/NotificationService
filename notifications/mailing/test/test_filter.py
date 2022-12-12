from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


class FilterTestCase(APITestCase):
    """
    Test Cases for :model:`mailing.Filter`
    """
    create_filter_url = reverse('create-filter')

    def test_create_filter(self):
        """
        Test POST create filter endpoint.
        """
        json_1 = {
            "filter_type": "Operator",
            "filter_value": "900"

        }
        json_2 = {
            "filter_type": "Operator",
            "filter_value": "asdf"

        }
        response_1 = self.client.post(
            self.create_filter_url,
            data=json_1,
        )
        response_2 = self.client.post(
            self.create_filter_url,
            data=json_2,
        )
        self.assertEqual(
            response_1.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response_2.status_code,
            status.HTTP_400_BAD_REQUEST
        )
