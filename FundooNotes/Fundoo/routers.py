from Fundoonotes.viewsets import NoteViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('notes', NoteViewSet)
