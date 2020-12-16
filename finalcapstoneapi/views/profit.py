"""View module for handling requests about supplies"""
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



class Profit(ViewSet):

    def list(self, request):
        user = User.objects.get(id=request.auth.user.id)
        categories = Category.objects.annotate(profit=Sum(
            F('items__shipping_paid') + F('items__item_paid') - F(
            'items__item_cost') - F('items__shipping_cost') - F('items__listing_fee') - F('items__final_value_fee'),
            filter=Q(items__user=user)
            ))
        print(categories.query)

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


