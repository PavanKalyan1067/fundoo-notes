from django.urls import path
from labels.views import LabelAPIView, UpdateLabelsAPIView, DeleteAPIView

urlpatterns = [
    path('api/create/', LabelAPIView.as_view(), name="create-label"),
    path('api/update/<int:pk>/', UpdateLabelsAPIView.as_view(), name="update-label"),
    path('api/delete/<int:pk>/', DeleteAPIView.as_view(), name="delete-label"),

]
