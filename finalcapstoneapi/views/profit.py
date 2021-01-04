"""View module for handling requests about supplies"""
from finalcapstoneapi.models.listing_type import Listing_Type
from django.db.models.aggregates import Sum
from finalcapstoneapi.models.item import Item
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from finalcapstoneapi.models import Expenses, Supply_Type, Category
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models import Q


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Category
        fields = ('name', 'profit')

class ListingTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Listing_Type
        fields = ('name', 'profit')

class TotalProfitSerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Item
        fields = ('profit', )



class ProfitByCategory(ViewSet):

    def list(self, request):
        user = User.objects.get(id=request.auth.user.id)
        categories = Category.objects.annotate(profit=Sum(
            F('categoryitems__shipping_paid') + F('categoryitems__item_paid') - F(
            'categoryitems__item_cost') - F('categoryitems__shipping_cost') - F('categoryitems__listing_fee') - F('categoryitems__final_value_fee'),
            filter=Q(categoryitems__user=user)
            ))
        print(categories.query)

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    def profit_by_category_filter_by_year(self, request):
        filteredcategories = []
        itemList = Item.objects.all()
        yearslist = list(itemList.sold_date)
        print(yearslist)
        # user = User.objects.get(id=request.auth.user.id)
        # categories = Category.objects.annotate(profit=Sum(
        #     F('categoryitems__shipping_paid') + F('categoryitems__item_paid') - F(
        #     'categoryitems__item_cost') - F('categoryitems__shipping_cost') - F('categoryitems__listing_fee') - F('categoryitems__final_value_fee'),
        #     filter=Q(categoryitems__user=user)
        #     ))
        # for years in self.date_purchased('%Y'):
        #     filteredcategories = categories.annotate(F('categoryitems__date_purchased = years'))

class ProfitByListingType(ViewSet):
    def list(self, request):
        user = User.objects.get(id=request.auth.user.id)

        listingtypes = Listing_Type.objects.annotate(profit=Sum(
            F('listingitems__shipping_paid') + F('listingitems__item_paid') - F(
            'listingitems__item_cost') - F('listingitems__shipping_cost') - F('listingitems__listing_fee') - F('listingitems__final_value_fee'),
            filter=Q(listingitems__user=user)
            ))
        print(listingtypes.query)

        serializer = ListingTypeSerializer(
            listingtypes, many=True, context={'request': request})
        return Response(serializer.data)

