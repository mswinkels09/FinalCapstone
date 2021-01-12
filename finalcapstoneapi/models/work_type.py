from django.db import models


class Work_Type(models.Model):
    """Work Type database model"""
    type = models.CharField(max_length=55)