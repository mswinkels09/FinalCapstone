from django.db import models


class Listing_Type(models.Model):
    """Listing Type database model"""
    name = models.CharField(max_length=55)

# unmapped property to use as a reference to calculate the total profit by listing type
    @property
    def profit(self, pk=None):
        return self.__profit

    @profit.setter
    def profit(self, value):
        self.__profit=value