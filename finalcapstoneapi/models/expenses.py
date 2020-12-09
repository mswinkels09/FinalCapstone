from django.db import models
from django.contrib.auth.models import User

class Expenses(models.Model):
    """Item database model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_purchased = models.DateField(auto_now=False, auto_now_add=False)
    cost = models.FloatField()
    supply_type = models.ForeignKey("Supply_Type", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='receipt_image', height_field=None, width_field=None, max_length=None, null=True)
