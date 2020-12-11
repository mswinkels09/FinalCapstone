"""View module for handling requests about supplies"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from finalcapstoneapi.models import Weight_Type, weight_type
from django.contrib.auth.models import User


class CurrentUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fields = ('id', )

class Weight_TypeSerializer(serializers.ModelSerializer):
    """JSON serializer for Weight_Type

    Arguments:
        serializers
    """
    user = CurrentUserSerializer(many=False)
    class Meta:
        model = Weight_Type
        fields = ('id', 'user', 'type', 'percentage')


class Weight_Types(ViewSet):

    def list(self, request):
        """Handle GET requests to Weight_Type resource"""
    
        weighttypes = Weight_Type.objects.all()

        serializer = Weight_TypeSerializer(
                weighttypes, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request to one Weight_Type"""

        try:
            weight_Type = Weight_Type.objects.get(pk=pk)
            serializer = Weight_TypeSerializer(weight_Type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations for weight_types

        Returns:
            Response -- JSON serialized weight_type instance
        """
        weight_type = Weight_Type()

        user = User.objects.get(id=request.auth.user.id)
        weight_type.user = user
        weight_type.type = request.data["type"]
        weight_type.percentage = request.data["percentage"]

        try:
            weight_type.save()
            serializer = Weight_TypeSerializer(weight_type, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single weight type
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            weight_type = Weight_Type.objects.get(pk=pk)
            weight_type.delete()
            #if succesful it will return a status code of 204
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        #if the object to be deleted doesn't exist status code will be 404
        except Weight_Type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)