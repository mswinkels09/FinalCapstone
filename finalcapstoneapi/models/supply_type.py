from django.db import models


class Supply_Type(models.Model):

    name = models.CharField(max_length=55)