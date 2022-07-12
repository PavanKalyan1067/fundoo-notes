from django.urls import path
from labels.views import LabelAPIView, UpdateLabelsAPIView

urlpatterns = [
    path('api/create', LabelAPIView.as_view()),
    path('api/update/<pk>', UpdateLabelsAPIView.as_view()),
]
