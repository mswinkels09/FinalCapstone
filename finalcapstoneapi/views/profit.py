"""View module for handling requests about supplies"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from finalcapstoneapi.models import Expenses, Supply_Type
from django.contrib.auth.models import User

class Profit(ViewSet):
    pass