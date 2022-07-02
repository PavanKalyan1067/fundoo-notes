from django.db import models
# from django.contrib.auth.models import User
from users.models import User

# Create your models here.
from labels.models import Labels


class Notes(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_created=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    label = models.ManyToManyField(Labels)
    isArchive = models.BooleanField(default=False, )
    isTrash = models.BooleanField(default=True, )
    isPinned = models.BooleanField(default=False, )
