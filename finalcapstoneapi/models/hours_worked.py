from django.db import models
from django.contrib.auth.models import User

class Hours_Worked(models.Model):
    """Hours Worked database model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    hours = models.FloatField()
    work_type = models.ForeignKey("Work_Type", on_delete=models.CASCADE)