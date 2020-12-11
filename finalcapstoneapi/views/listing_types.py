"""View module for handling requests about supplies"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from finalcapstoneapi.models import Listing_Type


class Listing_TypeSerializer(serializers.ModelSerializer):
    """JSON serializer for Listing_Type

    Arguments:
        serializers
    """
    class Meta:
        model = Listing_Type
        fields = ('id', 'name')


class Listing_Types(ViewSet):

    def list(self, request):
        """Handle GET requests to listing_Type resource"""
    
        listings = Listing_Type.objects.all()

        serializer = Listing_TypeSerializer(
                listings, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request to one Listing_Type"""

        try:
            listing_Type = Listing_Type.objects.get(pk=pk)
            serializer = Listing_TypeSerializer(listing_Type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)