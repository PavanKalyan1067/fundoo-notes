from django.urls import path
from labels.views import LabelAPIView

urlpatterns = [
    path('api/create', LabelAPIView.as_view()),
]
