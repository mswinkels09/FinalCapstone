from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    """Item database model"""


    """User will need the following when first creating a new item"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    unique_item_id = models.IntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    listing_type = models.ForeignKey("Listing_Type", on_delete=models.CASCADE)
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
    returned = models.BooleanField()
