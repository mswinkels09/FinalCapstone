from finalcapstoneapi.models.supply_type import Supply_Type
import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from finalcapstoneapi.models import Supply_Type

class Supply_Type_Tests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample supply_type
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "first_name": "Steve", "last_name": "Brownlee"}

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_supply_(self):
        """
        Ensure we can retrieve a supply_type.
        """
        #Seed the database with a supply_type
        supply_type = Supply_Type()
        supply_type.id = 1
        supply_type.name = "Supplies"
        supply_type.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/supply_types/{supply_type.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Supplies")
    
    def test_get_all_supply_(self):
        """
        Ensure we can retrieve all supply_types.
        """
        #Seed the database with a supply_type
        supply_type = Supply_Type()
        supply_type.id = 1
        supply_type.name = "Supplies"
        supply_type.save()

        supply_type= Supply_Type()
        supply_type.id = 2
        supply_type.name = "Inventory"
        supply_type.save()


        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/supply_types")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]["name"], "Supplies")
        self.assertEqual(json_response[1]["name"], "Inventory")


