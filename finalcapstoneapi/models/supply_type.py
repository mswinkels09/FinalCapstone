from django.db import models


class Supply_Type(models.Model):

    name = models.CharField(max_length=55)

    @property
    def expense(self, pk=None):
        return self.__expense

    @expense.setter
    def expense(self, value):
        self.__expense=value