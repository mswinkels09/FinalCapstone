"""View module for handling requests about supplies"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from finalcapstoneapi.models import Supply_Type


class Supply_TypeSerializer(serializers.ModelSerializer):
    """JSON serializer for Supply_Type

    Arguments:
        serializers
    """
    class Meta:
        model = Supply_Type
        fields = ('id', 'name')


class Supply_Types(ViewSet):

    def list(self, request):
        """Handle GET requests to supply_Type resource"""
    
        supplies = Supply_Type.objects.all()

        serializer = Supply_TypeSerializer(
                supplies, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request to one Supply_Type"""

        try:
            supply_Type = Supply_Type.objects.get(pk=pk)
            serializer = Supply_TypeSerializer(supply_Type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)