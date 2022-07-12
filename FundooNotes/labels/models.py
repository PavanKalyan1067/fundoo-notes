from django.db import models
from users.models import User


# Create your models here.

class Labels(models.Model):
    label = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.label

    REQUIRED_FIELDS = ['label']

