from django.db import models
from django.contrib.auth.models import User
from datetime import date

from django.db.models.aggregates import Count

class Item(models.Model):
    """Item database model"""


    """User will need the following when first creating a new item"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    unique_item_id = models.IntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="categoryitems")
    listing_type = models.ForeignKey("Listing_Type", on_delete=models.CASCADE,  related_name="listingitems")
    item_weight = models.FloatField()
    weight_type = models.ForeignKey("Weight_Type", on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, null=True)
    item_cost = models.FloatField()
    date_listed = models.DateField(auto_now=False, auto_now_add=False)
    listing_fee = models.FloatField()

    """User will fill out once item is sold"""
    shipping_cost = models.FloatField(blank=True, null=True)
    shipping_paid = models.FloatField(blank=True, null=True)
    item_paid = models.FloatField(blank=True, null=True)
    final_value_fee = models.FloatField(blank=True, null=True)
    sold_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    returned = models.BooleanField(blank=True, null=True)


# unmapped property will only be calculated when its sold
    @property
    def profit_per_item(self, pk=None):
        """Total profit of each item"""
        total_profit = 0
        total_cost = self.item_cost + self.shipping_cost + self.listing_fee + self.final_value_fee
        total_paid = self.shipping_paid + self.item_paid
        total_profit = total_paid - total_cost
        return total_profit

    @property
    def profit_per_item_percentage(self, pk=None):
        """Total profit of each item"""
        total_profit_percentage = 0
        total_cost = self.item_cost + self.shipping_cost + self.listing_fee + self.final_value_fee
        total_paid = self.shipping_paid + self.item_paid
        total_profit_percentage = round(100*((total_paid - total_cost) / total_cost), 2)
        return total_profit_percentage

    @property
    def profit(self, pk=None):
        return self.__profit

    @profit.setter
    def profit(self, value):
        self.__profit=value

    @property
    def profityear(self, pk=None):
        return self.__profityear

    @profityear.setter
    def profityear(self, value):
        self.__profityear=value

    @property
    def profitmonth(self, pk=None):
        return self.__profitmonth

    @profitmonth.setter
    def profitmonth(self, value):
        self.__profitmonth=value
    
    @property
    def soldItemMonth(self, pk=None):
        return self.__soldItemMonth

    @soldItemMonth.setter
    def soldItemMonth(self, value):
        self.__soldItemMonth=value
    
    @property
    def totalitems(self, pk=None):
        return self.__totalitems

    @totalitems.setter
    def totalitems(self, value):
        self.__totalitems=value

    @property
    def daysListed(self, pk=None):
        currentDate = date.today()
        d2 = self.date_listed
        return abs((currentDate-d2).days)

    @property
    def dateSoldConverted(self, pk=None):
        return self.sold_date.strftime('%m/%d/%Y')
