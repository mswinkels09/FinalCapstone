from django.conf import SettingsReference
from django.db import models


class Category(models.Model):
    """Category database model"""

    name = models.CharField(max_length=55)

# unmapped property to use as a reference to calculate the total profit by categories
    @property
    def profit(self, pk=None):
        return self.__profit

    @profit.setter
    def profit(self, value):
        self.__profit=value
        