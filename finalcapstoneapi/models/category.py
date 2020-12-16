from django.conf import SettingsReference
from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=55)

    @property
    def profit(self, pk=None):
        return self.__profit

    @profit.setter
    def profit(self, value):
        self.__profit=value
        