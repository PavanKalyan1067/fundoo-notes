from django.contrib import admin
from django.urls import path
from Fundoonotes.views import RetrieveAPIView,UpdateAPIView,DeleteAPIView,CreateAPIView

urlpatterns = [
    path('notesapi/retrieve', RetrieveAPIView.as_view()),
    path('notesapi/update', UpdateAPIView.as_view()),
    path('notesapi/delete', DeleteAPIView.as_view()),
    path('notesapi/create', CreateAPIView.as_view()),

]