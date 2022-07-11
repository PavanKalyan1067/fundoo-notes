from django.urls import path
from Fundoonotes.views import (
    RetrieveAPIView,
    UpdateNotesAPIView,
    DeleteAPIView,
    CreateAPIView,
    ArchiveNotesAPIView,
    AllArchiveNotesAPIView,
    AllTrashNotesAPIView,
    TrashNotesAPIView,
    AllPinNotesAPIView,
    PinNotesAPIView,

)

urlpatterns = [
    path('api/retrieve/', RetrieveAPIView.as_view()),
    path('api/update/<int:pk>/', UpdateNotesAPIView.as_view()),
    path('api/delete/<pk>/', DeleteAPIView.as_view()),
    path('api/create/', CreateAPIView.as_view()),
    path('api/archive/<pk>', ArchiveNotesAPIView.as_view()),
    path('api/archive1/', AllArchiveNotesAPIView.as_view()),
    path('api/trash/', AllTrashNotesAPIView.as_view()),
    path('api/trash1/<pk>', TrashNotesAPIView.as_view()),
    path('api/pin/<pk>', PinNotesAPIView.as_view()),
    path('api/pin1/', AllPinNotesAPIView.as_view()),

]
