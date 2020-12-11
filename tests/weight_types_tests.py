import json
from rest_framework import status
from rest_framework.test import APITestCase
from finalcapstoneapi.models import Weight_Type, weight_type

class Weight_Type_Tests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample weight_type
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "first_name": "Steve", "last_name": "Brownlee"}

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_weight_(self):
        """
        Ensure we can retrieve a weight_type.
        """
        #Seed the database with a weight_type
        weight_type = Weight_Type()
        weight_type.id = 1
        weight_type.type = "Books"
        weight_type.percentage = 0.59
        weight_type.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/weight_types/{weight_type.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the weight_type was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["type"], "Books")
    
    def test_get_all_weight_(self):
        """
        Ensure we can retrieve all weight_types.
        """
        #Seed the database with a weight_type
        weight_type = Weight_Type()
        weight_type.id = 1
        weight_type.type = "Books"
        weight_type.percentage = 0.59
        weight_type.save()

        weight_type= Weight_Type()
        weight_type.id = 2
        weight_type.type = "Inventory"
        weight_type.percentage = 1.09
        weight_type.save()


        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/weight_types")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the weight_type was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]["type"], "Books")
        self.assertEqual(json_response[0]["percentage"], 0.59)
        self.assertEqual(json_response[1]["type"], "Inventory")
        self.assertEqual(json_response[1]["percentage"], 1.09)

    def test_create_weight_type(self):
        """
        Ensure we can create a new weight type.
        """
        # DEFINE WEIGHT TYPE PROPERTIES
        url = "/weight_types"
        data = {
            "user_id": 1,
            "type": "DVDs",
            "percentage": 0.75
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the weight type was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["type"], "DVDs")
        self.assertEqual(json_response["percentage"], 0.75)

    def test_delete_weight_type(self):
        """
        Ensure we can delete an existing weight type.
        """
        weight_type = Weight_Type()
        weight_type.user_id = 1
        weight_type.type = "CDs"
        weight_type.percentage = 0.75
        weight_type.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/weight_types/{weight_type.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # DELETE weight_type AGAIN TO VERIFY 404 response
        response = self.client.delete(f"/weight_types/{weight_type.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



