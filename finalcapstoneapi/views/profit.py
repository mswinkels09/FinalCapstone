"""View module for handling requests about supplies"""
from django.db.models.functions.datetime import ExtractMonth, ExtractYear
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
from datetime import datetime


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories and total profit"""
    class Meta:
        model = Category
        fields = ('name', 'profit')


class ListingTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for listing types and total profit"""
    class Meta:
        model = Listing_Type
        fields = ('name', 'profit')


class TotalProfitSerializer(serializers.ModelSerializer):
    """JSON serializer for total profit off of Item Model"""
    class Meta:
        model = Item
        fields = ('profit', )


class ProfitByYearSerializer(serializers.ModelSerializer):
    """JSON serializer for total profit and profit year off the Item Model"""
    class Meta:
        model = Item
        fields = ('profit', 'profityear')


class ProfitByMonthSerializer(serializers.ModelSerializer):
    """JSON serializer for total profit and profit month off the Item Model"""
    class Meta:
        model = Item
        fields = ('profit', 'profitmonth')


class ProfitByCategory(ViewSet):
    """Handle GET requests to Category resource - groups Category resource by categories and total profit
        SQL Statement: "
        Select Sum(TotalPaid - TotalCost) as TotalProfit,
        ItemTitle,
        CategoryName
        From (
            SELECT i.item_cost + i.shipping_cost + i.listing_fee + i.final_value_fee as TotalCost,
                i.item_paid + i.shipping_paid as TotalPaid,
                i.title as ItemTitle,
                c.name as CategoryName
            From finalcapstoneapi_item as i
                Join finalcapstoneapi_category c on c.id = i.category_id
            WHERE sold_date is not NULL
            )
        Group BY CategoryName;
        "
    """
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

class ProfitByListingType(ViewSet):
    """Handle GET requests to Listing Type resource - groups Listing Type resource by listing types and total profit
        SQL Statement: "
        Select Sum(TotalPaid - TotalCost) as TotalProfit,
        ItemTitle,
        ListingTypeName
        From (
            SELECT i.item_cost + i.shipping_cost + i.listing_fee + i.final_value_fee as TotalCost,
                i.item_paid + i.shipping_paid as TotalPaid,
                i.title as ItemTitle,
                l.name as ListingTypeName
            From finalcapstoneapi_item as i
                Join finalcapstoneapi_listing_type l on l.id = i.listing_type_id
            WHERE sold_date is not NULL
            )
        Group BY ListingTypeName;
        "
    """
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


class ProfitByYear(ViewSet):
    """Handle GET requests to Item resource - groups Item resource by year and total profit
        SQL Statement: "
        Select Sum(TotalPaid - TotalCost) as TotalProfit,
        Year
        From (
            SELECT i.item_cost + i.shipping_cost + i.listing_fee + i.final_value_fee as TotalCost,
                i.item_paid + i.shipping_paid as TotalPaid,
                strftime('%Y', sold_date) as Year
            From finalcapstoneapi_item as i
            WHERE sold_date is not NULL
            )
        Group BY Year;
        "
    """
    def list(self, request):
        user = User.objects.get(id=request.auth.user.id)
        profityears = Item.objects.values('sold_date__year').annotate(profit=Sum(
            F('shipping_paid') + F('item_paid') - F(
                'item_cost') - F('shipping_cost') - F('listing_fee') - F('final_value_fee')), profityear=ExtractYear('sold_date__year')).filter(Q(user=user) & Q(sold_date__isnull=False))

        serializer = ProfitByYearSerializer(
            profityears, many=True, context={'request': request})
        return Response(serializer.data)


class ProfitByMonth(ViewSet):
    """Handle GET requests to Item resource - groups Item resource by month and total profit
        SQL Statement: "
            select strftime('%m', sold_date) as Month, 
            sum(cost)
            from finalcapstoneapi_item
            where strftime('%Y', sold_date) = strftime('%Y',date('now'))
            group by strftime('%m', sold_date)
            order by Month;
        "
    """
    def list(self, request):
        user = User.objects.get(id=request.auth.user.id)
        currentYear = datetime.now().year
        profitmonths = Item.objects.values('sold_date__month').annotate(profit=Sum(
            F('shipping_paid') + F('item_paid') - F(
                'item_cost') - F('shipping_cost') - F('listing_fee') - F('final_value_fee')), profitmonth=ExtractMonth('sold_date__month')).filter(Q(user=user) & Q(sold_date__isnull=False) & (Q(sold_date__contains=currentYear)))

        serializer = ProfitByMonthSerializer(
            profitmonths, many=True, context={'request': request})
        return Response(serializer.data)
