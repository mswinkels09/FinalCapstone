"""View module for handling requests about listed items"""
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from finalcapstoneapi.models import Item, Category, Listing_Type, Weight_Type

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Category
        fields = ('name', )

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fields = ('id', )

class ListingTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for listing types"""
    class Meta:
        model = Listing_Type
        fields = ('name', )

class WeightTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for listing types"""
    class Meta:
        model = Weight_Type
        fields = ('type', 'percentage')


class ListedItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items"""
    user = UserSerializer(many=False)
    category = CategorySerializer(many=False)
    listing_type = ListingTypeSerializer(many=False)
    weight_type = WeightTypeSerializer(many=False)

    class Meta:
        model = Item
        fields = ('id', 'user', 'title', 'unique_item_id', 'category', 'listing_type',
                'item_weight', 'weight_type', 'notes', 'item_cost','date_listed', 
                'listing_fee', )
        depth = 1



class ListedItems(ViewSet):
    """Request handlers for listed items"""

    def create(self, request):
        """
        @api {item} /listeditems item new item
        @apiName CreateListedItem
        @apiGroup ListedItems

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {Number} user_id - Current user that is authenticated
        @apiParam {String} title - Name of the item being listed
        @apiParam {Number} unique_item_id - Form of id given from the website where the user is listing the item
        @apiParam {Number} category_id - Category of item
        @apiParam {Number} listing_type_id - What kind of listing is the user using to sell the item
        @apiParam {Number} item_weight - How much the item weighs
        @apiParam {Number} weight_type_id - Id that corresponds to a percentage that will help calculate the cost of the item(if applicable)
        @apiParam {String} notes - Any notes that the user wants to keep track of
        @apiParam {Number} item_cost - How much the item cost to buy initially (sometimes calculated using weight_type)
        @apiParam {String} date_listed - When the user listed the item
        @apiParam {Number} listing_fee - How much did it cost to list the item(if applicable)

        @apiParamExample {json} Input
            {
                "user_id": 1,
                "title": "12 inch Baby Yoda The Mandalorian Master Stuffed Doll Plush Toys Black Friday US SAL",
                "unique_item_id": 264954766269,
                "category_id": 1,
                "listing_type_id": 2,
                "item_weight": 165,
                "weight_type_id": 3,
                "notes": null,
                "item_cost": 2,
                "date_listed": "2020-12-09",
                "listing_fee": 0.30
            }

        @apiSuccess (200) {Object} item - Created item
        @apiSuccess (200) {id} item.id - Item Id
        @apiSuccess (200) {String} item.title - Name of the item being listed
        @apiSuccess (200) {Number} item.unique_item_id - Form of id given from the website where the user is listing the item
        @apiSuccess (200) {Number} item.category_id - Category of item
        @apiSuccess (200) {Number} item.listing_type_id - What kind of listing is the user using to sell the item
        @apiSuccess (200) {Number} item.item_weight - How much the item weighs
        @apiSuccess (200) {Number} item.weight_type_id - Id that corresponds to a percentage that will help calculate the cost of the item(if applicable)
        @apiSuccess (200) {String} item.notes - Any notes that the user wants to keep track of
        @apiSuccess (200) {Number} item.item_cost - How much the item cost to buy initially (sometimes calculated using weight_type)
        @apiSuccess (200) {Date} item.date_listed - When the user listed the item
        @apiSuccess (200) {Number} item.listing_fee - How much did it cost to list the item(if applicable)
        
        @apiSuccess (200) {Number} item.shipping_cost - How must the user paid for shipping
        @apiSuccess (200) {Number} item.shipping_paid - How much the customer paid for shipping
        @apiSuccess (200) {Number} item.item_paid - How much the customer paid for the item
        @apiSuccess (200) {Number} item.final_value_fee - Percentage of profit the website took out as a charge for selling an item on their website (if applicable)
        @apiSuccess (200) {Date} item.sold_date - Date item was sold
        @apiSuccess (200) {Boolean} item.returned - Changes to True if item was ever returned back to the user
        @apiSuccessExample {json} Success
            {
                "id": 101,
                "user_id": 1,
                "title": "12 inch Baby Yoda The Mandalorian Master Stuffed Doll Plush Toys Black Friday US SAL",
                "unique_item_id": 264954766269,
                "category_id": {
                    "name": "Toys"
                },
                "listing_type_id": {
                    "name": "Ebay: Buy It Now"
                },
                "item_weight": 165,
                "weight_type_id": {
                    "user_id": 1
                    "type": "N/A",
                    "percentage": 1
                },
                "notes": null,
                "item_cost": 2,
                "date_listed": "2020-12-09",
                "listing_fee": 0.30,
                "shipping_cost": null,
                "item_paid": null,
                "final_value_fee": null,
                "sold_date": null,
                "returned": "False"
            }
        """
        new_item = Item()
        new_item.title = request.data["title"]
        new_item.unique_item_id = request.data["unique_item_id"]
        new_item.item_weight = request.data["item_weight"]
        new_item.notes = request.data["notes"]
        new_item.item_cost = request.data["item_cost"]
        new_item.date_listed = request.data["date_listed"]
        new_item.listing_fee = request.data["listing_fee"]


        user = User.objects.get(id=request.auth.user.id)
        new_item.user = user

        item_category = Category.objects.get(pk=request.data["category_id"])
        new_item.category = item_category
        
        item_listing_type = Listing_Type.objects.get(pk=request.data["listing_type_id"])
        new_item.listing_type = item_listing_type
        
        item_weight_type = Weight_Type.objects.get(pk=request.data["weight_type_id"])
        new_item.weight_type = item_weight_type

        new_item.save()

        serializer = ListedItemSerializer(
            new_item, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def list(self, request):
        """
        @api {GET} /items GET all items
        @apiName ListListedItems
        @apiGroup ListedItems

        @apiSuccess (200) {Object[]} items Array of items
        @apiSuccessExample {json} Success
            [
                {
                    "id": 101,
                    "url": "http://localhost:8000/items/101",
                    "user_id": 1,
                    "title": "12 inch Baby Yoda The Mandalorian Master Stuffed Doll Plush Toys Black Friday US SAL",
                    "unique_item_id": 264954766269,
                    "category_id": {
                        "url": "http://localhost:8000/categories/1",
                        "name": "Toys"
                    },
                    "listing_type_id": {
                        "url": "http://localhost:8000/listing_type/2",
                        "name": "Ebay: Buy It Now"
                    },
                    "item_weight": 165,
                    "weight_type_id": {
                        "url": "http://localhost:8000/weight_type/3",
                        "type": "N/A",
                        "percentage": 1
                    },
                    "notes": null,
                    "item_cost": 2,
                    "date_listed": "2020-12-09",
                    "listing_fee": 0.30,
                    "shipping_cost": null,
                    "item_paid": null,
                    "final_value_fee": null,
                    "sold_date": null,
                    "returned": "False"
                }
            ]
        """

        current_user = User.objects.get(id=request.auth.user.id)
        items = Item.objects.filter(user=current_user, sold_date=None)

        json_items = ListedItemSerializer(
            items, many=True, context={'request': request})


        return Response(json_items.data)

    def retrieve(self, request, pk=None):
        """
        @api {GET} /listeditems/:id GET listed_item
        @apiName GetListedItem
        @apiGroup ListedItems

        @apiParam {id} id Item Id

        @apiSuccess (200) {Object{}} listed_item object
        @apiSuccessExample {json} Success
            {
                "id": 101,
                "user_id": 1,
                "title": "12 inch Baby Yoda The Mandalorian Master Stuffed Doll Plush Toys Black Friday US SAL",
                "unique_item_id": 264954766269,
                "category_id": {
                    "name": "Toys"
                },
                "listing_type_id": {
                    "name": "Ebay: Buy It Now"
                },
                "item_weight": 165,
                "weight_type_id": {
                    "user_id": 1
                    "type": "N/A",
                    "percentage": 1
                },
                "notes": null,
                "item_cost": 2,
                "date_listed": "2020-12-09",
                "listing_fee": 0.30,
                "shipping_cost": null,
                "item_paid": null,
                "final_value_fee": null,
                "sold_date": null,
                "returned": "False"
            }
        """
        try:
            # pk is a parameter to this function, and 
            # Django parses it from the URL rouote parameter
            # http://localhost:8000/items/2
            #
            # The `2` at the end of the route becomes `pk`
            user = User.objects.get(id=request.auth.user.id)
            item = Item.objects.get(pk=pk, user=user, sold_date=None)
            serializer = ListedItemSerializer(item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        @api {PUT} /listeditems/:id PUT update listed item
        @apiName UpdateListedItem
        @apiGroup ListedItems

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token fa2eba9be8282d595c997ee5cd49f2ed31f65be1

        @apiParam {id} id Listed Id route parameter
        @apiParam {Number} user_id - Current user that is authenticated
        @apiParam {String} title - Name of the item being listed
        @apiParam {Number} unique_item_id - Form of id given from the website where the user is listing the item
        @apiParam {Number} category_id - Category of item
        @apiParam {Number} listing_type_id - What kind of listing is the user using to sell the item
        @apiParam {Number} item_weight - How much the item weighs
        @apiParam {Number} weight_type_id - Id that corresponds to a percentage that will help calculate the cost of the item(if applicable)
        @apiParam {String} notes - Any notes that the user wants to keep track of
        @apiParam {Number} item_cost - How much the item cost to buy initially (sometimes calculated using weight_type)
        @apiParam {String} date_listed - When the user listed the item
        @apiParam {Number} listing_fee - How much did it cost to list the item(if applicable)
        @apiParamExample {json} Input
            {
                "user_id": 1,
                "title": "12 inch Baby Yoda The Mandalorian Master Stuffed Doll Plush Toys Black Friday US SAL",
                "unique_item_id": 264954766269,
                "category_id": 1,
                "listing_type_id": 2,
                "item_weight": 165,
                "weight_type_id": 3,
                "notes": null,
                "item_cost": 2,
                "date_listed": "2020-12-09",
                "listing_fee": 0.30
            }

        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """

        user = User.objects.get(id=request.auth.user.id)

        listed_item = Item.objects.get(pk=pk)
        listed_item.title = request.data['title']
        listed_item.unique_item_id = request.data['unique_item_id']
        listed_item.item_weight = request.data['item_weight']
        listed_item.notes = request.data['notes']
        listed_item.item_cost = request.data['item_cost'] # will need help getting this right
        listed_item.user = user

        category = Category.objects.get(pk=request.data["category_id"])
        listed_item.category = category

        listing_type= Listing_Type.objects.get(pk=request.data["listing_type_id"])
        listed_item.listing_type = listing_type

        weight_type = Weight_Type.objects.get(pk=request.data["weight_type_id"])
        listed_item.weight_type = weight_type

        listed_item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """
        @api {DELETE} /listeditems/:id DELETE line item from cart
        @apiName DeleteListedItem
        @apiGroup ListedItems

        @apiParam {id} id Item Id to remove from cart
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        try:
            listed_item = Item.objects.get(pk=pk, sold_date=None)
            listed_item.delete()
            #if succesful it will return a status code of 204
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        #if the object to be deleted doesn't exist status code will be 404
        except Item.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
