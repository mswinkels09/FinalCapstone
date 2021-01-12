from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Expenses(models.Model):
    """Expense database model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_purchased = models.DateField(auto_now=False, auto_now_add=False)
    cost = models.FloatField()
    supply_type = models.ForeignKey("Supply_Type", on_delete=models.CASCADE, related_name="expenses")
    image = models.ImageField(upload_to='receipt_image', height_field=None, width_field=None, max_length=None, null=True)
    
# unmapped property to use as a reference to calculate the total expense for the current year
    @property
    def totalexpense(self, pk=None):
        return self.__expense

# unmapped property to use as a reference to the months in date_purchased - to calculate the total expense by month of current year
    @property
    def expensemonth(self, pk=None):
        return self.__expense
    
# unmapped property to use as a reference to convert to %m/%d/%Y from yyyy-mm-dd
    @property
    def dateExpenseConverted(self, pk=None):
        return self.date_purchased.strftime('%m/%d/%Y')

