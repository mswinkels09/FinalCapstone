from finalcapstoneapi.models.listing_type import Listing_Type
import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from finalcapstoneapi.models import Listing_Type

class Listing_Type_Tests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample listing_type
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "first_name": "Steve", "last_name": "Brownlee"}

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_listing_(self):
        """
        Ensure we can retrieve a listing_type.
        """
        #Seed the database with a listing_type
        listing_type = Listing_Type()
        listing_type.id = 1
        listing_type.name = "Ebay: Auction"
        listing_type.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/listing_types/{listing_type.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Ebay: Auction")
    
    def test_get_all_listing_(self):
        """
        Ensure we can retrieve all listing_types.
        """
        #Seed the database with a listing_type
        listing_type = Listing_Type()
        listing_type.id = 1
        listing_type.name = "Ebay: Auction"
        listing_type.save()

        listing_type= Listing_Type()
        listing_type.id = 2
        listing_type.name = "Ebay: Buy It Now"
        listing_type.save()


        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/listing_types")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]["name"], "Ebay: Auction")
        self.assertEqual(json_response[1]["name"], "Ebay: Buy It Now")


