from django.urls import path
from labels.views import LabelAPIView, UpdateLabelsAPIView, DeleteAPIView

urlpatterns = [
    path('api/create/', LabelAPIView.as_view()),
    path('api/update/<pk>/', UpdateLabelsAPIView.as_view()),
    path('api/delete/<pk>/', DeleteAPIView.as_view()),

]
