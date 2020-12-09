from django.db import models


class Work_Type(models.Model):

    type = models.CharField(max_length=55)