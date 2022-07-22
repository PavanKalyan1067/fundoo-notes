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
    DisplayNoteByLabelView,
    CollaboratedNoteView,
    LabelNoteView,

)

urlpatterns = [
    path('api/retrieve/', RetrieveAPIView.as_view(), name="retrieve"),
    path('api/update/<int:pk>/', UpdateNotesAPIView.as_view(), name="update-notes"),
    path('api/delete/<int:pk>/', DeleteAPIView.as_view(), name="delete-notes"),
    path('api/create/', CreateAPIView.as_view(), name="create-notes"),
    path('api/archive/<int:pk>', ArchiveNotesAPIView.as_view(), name="archive"),
    path('api/all-archive-notes/', AllArchiveNotesAPIView.as_view(), name="all-archive-notes"),
    path('api/all-trash-notes/', AllTrashNotesAPIView.as_view(), name="all-trash-notes"),
    path('api/trash/<int:pk>', TrashNotesAPIView.as_view(), name="trash"),
    path('api/pin/<int:pk>', PinNotesAPIView.as_view(), name="pin"),
    path('api/all-pin-notes/', AllPinNotesAPIView.as_view(), name="all-pin-notes"),
    path('api/display/<label>', DisplayNoteByLabelView.as_view(), name="display"),
    path('api/collaborated/note/', CollaboratedNoteView.as_view(), name="collaborated-note"),
    path('api/label/note/', LabelNoteView.as_view(), name="label-note"),

]
