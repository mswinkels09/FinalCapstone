from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from finalcapstoneapi.models import Item, Category, Listing_Type, Weight_Type
from finalcapstoneapi.views.listeditems import CategorySerializer, WeightTypeSerializer, ListingTypeSerializer, UserSerializer

class SoldItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items"""
    user = UserSerializer(many=False)
    category = CategorySerializer(many=False)
    listing_type = ListingTypeSerializer(many=False)
    weight_type = WeightTypeSerializer(many=False)

    class Meta:
        model = Item
        fields = ('id', 'user', 'title', 'unique_item_id', 'category', 'listing_type',
                'item_weight', 'weight_type', 'notes', 'item_cost','date_listed', 
                'listing_fee', 'shipping_cost', 'shipping_paid', 'item_paid', 
                'final_value_fee', 'sold_date', 'returned', )
        depth = 1


class SoldItems(ViewSet):
    """Request handlers for sold items"""
    def list(self, request):
        """
        @api {GET} /solditems GET all sold items
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
                    "shipping_cost": 8.50,
                    "shipping_paid": 12,
                    "item_paid": 15,
                    "final_value_fee": 1,
                    "sold_date": "2020-12-12",
                    "returned": "False"
                }
            ]
        """

        user = User.objects.get(id=request.auth.user.id)
        try:
            solditems = Item.objects.filter(user=user, sold_date__isnull=False)
            json_items = SoldItemSerializer(
                solditems, many=True, context={'request': request})
            return Response(json_items.data)
        except Item.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
