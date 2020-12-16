from django.db import models
from django.contrib.auth.models import User
import datetime

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
        total_profit_percentage = 100*((total_paid - total_cost) / total_cost)
        return total_profit_percentage

    @property
    def profit(self, pk=None):
        return self.__profit

    @profit.setter
    def profit(self, value):
        self.__profit=value

    # @property
    # def profit_per_month(self, pk=None):
    #     """Total profit per month"""
    #     date_sold = self.sold_date
    #     year,month,date = date_sold.split('-')
    #     for year in datetime.date[0]:
    #         for month in datetime.date[1]:
    #             total_profit = 0
    #             self.profit_per_item += total_profit
    #             return total_profit
