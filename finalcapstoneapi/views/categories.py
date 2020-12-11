"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from finalcapstoneapi.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for Category

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'name')


class Categories(ViewSet):

    def list(self, request):
        """Handle GET requests to category resource"""
    
        categories = Category.objects.all()

        serializer = CategorySerializer(
                categories, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request to one category"""

        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)