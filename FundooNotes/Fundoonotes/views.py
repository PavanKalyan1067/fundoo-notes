from django.core.cache import cache
from django.http import Http404
from django.http.multipartparser import MultiPartParser
from django.utils import timezone
from rest_framework import serializers, status, generics, permissions, request
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from users.models import User
from .logger import get_logger
from .models import Notes
from Fundoonotes.exceptions import DoesNotExist, validate_time, DoesNotExistException, PassedTimeException
from rest_framework.views import APIView
from .serializers import NotesSerializer
from Fundoonotes.Response import response_code

logger = get_logger()


def get_user(token):
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    newToken = str(token).split("Bearer ")[1]
    encodedToken = jwt_decode_handler(newToken)
    username = encodedToken['username']
    user = User.objects.get(username=username)
    return user.id


class CreateAPIView(generics.GenericAPIView):
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            serializer = NotesSerializer(data=request.data, partial=True)
            serializer.is_valid()
            serializer.save(user_id=user.id)
            data = serializer.data
            response = {
                'success': True,
                'message': response_code[201],
                'data': data
            }
            return Response(response)

        except ValidationError as e:
            response = {
                'success': False,
                'message': response_code[308],
            }
            logger.exception(e)
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416], }
            logger.exception(e)
            return Response(response)


class RetrieveAPIView(APIView):
    def get(self, request, pk):
        try:
            data = Notes.objects.all()

            # data = Notes.objects.get(pk=pk)
            logger.info('Getting the notes data on %s', timezone.now())
            serializer = NotesSerializer(data, many=True)
            serialized_data = serializer.data
            response = {
                'success': True,
                'message': response_code[200],
                'data': serialized_data,
            }
            return Response(response)
        except DoesNotExist as e:
            response = {
                'success': False,
                'message': response_code[307]
            }
            logger.exception(e)
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416],
            }
            logger.exception(e)
            return Response(response)


class DeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            data = Notes.objects.get(pk=pk)
            data.delete()
            response = {
                'success': True,
                'message': response_code[200],
            }
            return Response(response)
        except DoesNotExist as e:
            response = {
                'success': False,
                'message': response_code[307]
            }
            logger.exception(e)
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416],
            }
            logger.exception(e)
            return Response(response)


class UpdateNotesApiView(generics.GenericAPIView):
    serializer_class = NotesSerializer
    data = Notes.objects.all()

    def get_objects(self, pk):
        try:
            return Notes.objects.get(pk=pk)
        except Exception:
            response = {
                'success': False,
                'message': response_code[416],
            }
            return Response(response)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        note = self.get_objects(pk=pk)
        serializer = NotesSerializer(note)
        response = {
            'success': True,
            'message': response_code[200],
            'data': serializer.data
        }
        return Response(response)

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        note = self.get_objects(pk=pk)
        serializer = NotesSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            note = Notes.objects.get(pk=pk)
            if note.isArchive:
                note.isPinned = False
                note.save()
            response = {
                'success': True,
                'message': response_code[200],
                'data': serializer.data
            }
            return Response(response)
        response = {
            'success': False,
            'message': response_code[416],
        }
        return Response(response)
