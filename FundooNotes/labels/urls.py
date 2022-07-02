from django.contrib import admin
from django.urls import path
from labels.views import RetrieveAPIView,UpdateAPIView,DeleteAPIView,CreateAPIView

urlpatterns = [
    path('api/retrieve', RetrieveAPIView.as_view()),
    path('api/update', UpdateAPIView.as_view()),
    path('api/delete', DeleteAPIView.as_view()),
    path('api/create', CreateAPIView.as_view()),

]