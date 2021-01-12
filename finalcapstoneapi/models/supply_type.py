from django.db import models


class Supply_Type(models.Model):
    """Supply Type database model"""
    name = models.CharField(max_length=55)

# unmapped property to use as a reference to calculate the total expense by supply type
    @property
    def expense(self, pk=None):
        return self.__expense

    @expense.setter
    def expense(self, value):
        self.__expense=value