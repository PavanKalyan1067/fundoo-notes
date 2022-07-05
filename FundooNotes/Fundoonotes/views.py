import datetime
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers, status
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from users.models import User
from .logger import get_logger
from .models import Notes

# Create your views here.
from rest_framework.views import APIView

from .serializers import NotesSerializer
from .utils import get_notes_by_user_id
from rest_framework.exceptions import APIException

logger = get_logger()
from datetime import datetime
from rest_framework.exceptions import PassedTimeException

from Fundoonotes.Response import validate_time, response_code


class RetrieveAPIView(APIView):
    def get(self, request):
        try:
            data = Notes.objects.all()
            logger.info('Getting the notes data on %s', timezone.now())
            serializer = NotesSerializer(data, many=True)
            serialized_data = serializer.data
            response = {
                'success': True,
                'message': response_code[200],
                'data': serialized_data,
            }
            return Response(response, )
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416],
            }
            return Response(response)


class CreateAPIView(APIView):

    def post(self, request):
        try:
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            notes = Notes(title=serializer.data.get('title'), description=serializer.data.get('description'))
            notes.save()
            data = serializer.data
            response = {
                'success': True,
                'message': response_code[201],
                'data': {'notes_list': data}
            },
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416],
            }
            return Response(response)


class UpdateAPIView(APIView):
    def put(self, request, ):
        try:
            data = Notes.objects.get(pk=1)
            serializer = NotesSerializer(data, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # serialized_data = serializer.data
            response = {
                'success': True,
                'message': response_code[202],
                'data': {'notes_list': serializer.data},
            }
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416],
            }
        return Response(response)


class DeleteAPIView(APIView):
    def delete(self, request, ):
        try:
            data = Notes.objects.get(pk=2)
            data.delete()
            response = {
                'success': True,
                'message': response_code[200],
            }
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416],
            }
        return Response(response)
