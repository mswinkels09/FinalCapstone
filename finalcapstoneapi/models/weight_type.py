from django.db import models
from django.contrib.auth.models import User


class Weight_Type(models.Model):
    """Weight Type database model"""
    type = models.CharField(max_length=55)
    percentage = models.FloatField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)