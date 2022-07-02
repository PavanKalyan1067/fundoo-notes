from django.db import models
from users.models import User


# Create your models here.

class Labels(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_created=True,null=True)
    modified_at = models.DateTimeField(auto_now=True,null=True)
