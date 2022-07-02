from rest_framework import serializers, status
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .logger import get_logger
from .models import Notes

# Create your views here.
from rest_framework.views import APIView

from .serializers import NotesSerializer

logger = get_logger()


class RetrieveAPIView(APIView):
    def get(self, request):
        try:
            data = Notes.objects.all()
            serializer = NotesSerializer(data, many=True)
            serialized_data = serializer.data
            response = {
                'success': True,
                'data': serialized_data,
                'message': 'Successfully Retrieved all Data!',
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong! Please try again...'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CreateAPIView(APIView):
    def post(self, request, user_id):
        try:
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            notes = Notes(title=serializer.data.get('title'), description=serializer.data.get('description'),
                          user_id=user_id)
            notes.save()
            data = serializer.data
            # data.update({'id': notes.id})
            response = {
                'success': True,
                'message': 'Notes created successfully!',
                'data': {'notes_list': data}
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'message': 'Oops! Something went wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)


class UpdateAPIView(APIView):
    def put(self, request, ):
        try:
            data = Notes.objects.get(pk=1)
            serializer = NotesSerializer(data, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serialized_data = serializer.data
            response = {
                'status': 'Successfully Updated Data',
                'user': serialized_data,
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong! Please try again...'
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class DeleteAPIView(APIView):
    def delete(self, request, ):
        try:
            data = Notes.objects.get(pk=9)
            data.delete()
            response = {
                'status': 'Successfully Deleted Data',
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong! Please try again...'
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
