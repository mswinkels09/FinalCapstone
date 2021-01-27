from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from django.db.models.aggregates import Count

class Item(models.Model):
    """Item database model"""

    def validate_value(value):
        if value < 0:
            raise ValidationError("Please enter a number greater than 0")

    """User will need the following when first creating a new item"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    unique_item_id = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="categoryitems")
    listing_type = models.ForeignKey("Listing_Type", on_delete=models.CASCADE,  related_name="listingitems")
    item_weight = models.FloatField(validators=[validate_value])
    weight_type = models.ForeignKey("Weight_Type", on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, null=True, blank=True, default=None)
    item_cost = models.FloatField(validators=[validate_value])
    date_listed = models.DateField(auto_now=False, auto_now_add=False)
    listing_fee = models.FloatField(validators=[validate_value])

    """User will fill out once item is sold"""
    shipping_cost = models.FloatField(blank=True, null=True, validators=[validate_value])
    shipping_paid = models.FloatField(blank=True, null=True, validators=[validate_value])
    item_paid = models.FloatField(blank=True, null=True, validators=[validate_value])
    final_value_fee = models.FloatField(blank=True, null=True, validators=[validate_value])
    sold_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    returned = models.BooleanField(blank=True, null=True)


# unmapped property will only be calculated when its sold - calulates the profit after item is sold
    @property
    def profit_per_item(self, pk=None):
        """Total profit of each item"""
        total_profit = 0
        total_cost = self.item_cost + self.shipping_cost + self.listing_fee + self.final_value_fee
        total_paid = self.shipping_paid + self.item_paid
        total_profit = total_paid - total_cost
        return total_profit
# unmapped property will only be calculated when its sold - calculated the percentage of profit after item is sold
    @property
    def profit_per_item_percentage(self, pk=None):
        """Total profit of each item"""
        total_profit_percentage = 0
        total_cost = self.item_cost + self.shipping_cost + self.listing_fee + self.final_value_fee
        total_paid = self.shipping_paid + self.item_paid
        total_profit_percentage = round(100*((total_paid - total_cost) / total_cost), 2)
        return total_profit_percentage

# unmapped property to use as a reference to calculate the total profit
    @property
    def profit(self, pk=None):
        return self.__profit

    @profit.setter
    def profit(self, value):
        self.__profit=value

# unmapped property to use as a reference for the years in "sold_date" - to categorize the total profit by year
    @property
    def profityear(self, pk=None):
        return self.__profityear

    @profityear.setter
    def profityear(self, value):
        self.__profityear=value

# unmapped property to use as a reference for the months in "sold_date" - to categorize the total profit by month in the current year
    @property
    def profitmonth(self, pk=None):
        return self.__profitmonth

    @profitmonth.setter
    def profitmonth(self, value):
        self.__profitmonth=value
    
    # unmapped property to use as a reference for the months in "sold_date" - to categorize the total number of items sold per month of current year
    @property
    def soldItemMonth(self, pk=None):
        return self.__soldItemMonth

    @soldItemMonth.setter
    def soldItemMonth(self, value):
        self.__soldItemMonth=value
    
    # unmapped property to use as a reference to the number of items total -right now only categorizing them per month of current year
    @property
    def totalitems(self, pk=None):
        return self.__totalitems

    @totalitems.setter
    def totalitems(self, value):
        self.__totalitems=value

# unmapped property to use as a reference to the number of days a specific item has been listed on a platform since the current date
    @property
    def daysListed(self, pk=None):
        currentDate = date.today()
        d2 = self.date_listed
        return abs((currentDate-d2).days)

# unmapped property to use as a reference to the conversion of the sold_date property to %m/%d/%Y from yyyy-mm-dd
    @property
    def dateSoldConverted(self, pk=None):
        return self.sold_date.strftime('%m/%d/%Y')
