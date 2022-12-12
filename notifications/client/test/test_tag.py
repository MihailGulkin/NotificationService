from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class TagTestCase(APITestCase):
    """
    Test Cases for :model:`client.Tag`.
    """
    create_tag_url = reverse('create-tag')

    def test_create_tag(self):
        """
        Test POST create tag endpoint.
        """
        json = {
            "tag_name": "apple",
        }

        response = self.client.post(
            self.create_tag_url,
            data=json,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
