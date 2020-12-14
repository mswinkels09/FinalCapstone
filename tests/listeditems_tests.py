import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from finalcapstoneapi.models import Item


class ListedItemTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "first_name": "Steve", "last_name": "Brownlee"}

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_category(self):
    #     """
    #     Ensure we can retrieve a .
    #     """
    #     #Seed the database with a category
    #     category = Category()
    #     category.id = 1
    #     category.name = "Toys"
    #     category.save()

    #     # Make sure request is authenticated
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    #     # Initiate request and store response
    #     response = self.client.get(f"/categories/{category.id}")

    #     # Parse the JSON in the response body
    #     json_response = json.loads(response.content)

    #     # Assert that the game was retrieved
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Assert that the values are correct
    #     self.assertEqual(json_response["name"], "Toys")