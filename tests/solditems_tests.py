import json
from rest_framework import status
from rest_framework.test import APITestCase
from finalcapstoneapi.models import Item

# class SoldItemTests(APITestCase):
    # def setUp(self) -> None:
    #     """
    #     Create a new account and create sample category
    #     """
    #     url = "/register"
    #     data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
    #             "first_name": "Steve", "last_name": "Brownlee"}

    #     response = self.client.post(url, data, format='json')
    #     json_response = json.loads(response.content)
    #     self.token = json_response["token"]
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_category(self):
    #     """
    #     Ensure we can retrieve a category.
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
    
    # def test_get_all_category(self):
    #     """
    #     Ensure we can retrieve all categories.
    #     """
    #     #Seed the database with categories
    #     category = Category()
    #     category.id = 1
    #     category.name = "Toys"
    #     category.save()

    #     category = Category()
    #     category.id = 2
    #     category.name = "Books"
    #     category.save()


    #     # Make sure request is authenticated
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    #     # Initiate request and store response
    #     response = self.client.get(f"/categories")

    #     # Parse the JSON in the response body
    #     json_response = json.loads(response.content)

    #     # Assert that the game was retrieved
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Assert that the values are correct
    #     self.assertEqual(len(json_response), 2)
    #     self.assertEqual(json_response[0]["name"], "Toys")
    #     self.assertEqual(json_response[1]["name"], "Books")
