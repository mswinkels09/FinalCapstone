from django.db import models


class Weight_Type(models.Model):

    type = models.CharField(max_length=55)
    percentage = models.FloatField()