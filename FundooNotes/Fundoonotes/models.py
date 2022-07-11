from django.db import models
from users.models import User
from labels.models import Labels


class Notes(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    label = models.ManyToManyField(Labels)
    reminder = models.TimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    isArchive = models.BooleanField(default=False)
    isTrash = models.BooleanField(default=False)
    isPinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title
