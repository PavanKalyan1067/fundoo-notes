from django.core.cache import cache
from django.db.models import Q
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
from .serializers import NotesSerializer, TrashSerializer, PinSerializer
from Fundoonotes.Response import response_code
from .utils import get_notes_by_id

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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        try:
            note = Notes.objects.filter(user=request.user)
            serializer = NotesSerializer(note, many=True)
            logger.info('Getting the notes data on %s', timezone.now())
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


class UpdateNotesAPIView(generics.GenericAPIView):
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


class AllArchiveNotesAPIView(generics.GenericAPIView):
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            archives = Notes.objects.filter(user_id=user.id, isTrash=False, isArchive=True)
            serializer = NotesSerializer(archives, many=True)
            response = {
                "success": True,
                "msg": response_code[200],
                "data": serializer.data
            }
            return Response(response)
        except Exception:
            response = {
                "success": False,
                "msg": response_code[416],
            }
            return Response(response)


class ArchiveNotesAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwar):
        pk = self.kwargs.get('pk')
        note_id = pk
        note = Notes.objects.get(id=note_id)
        try:
            if not note.isArchive:
                note.isArchive = True
            else:
                note.isArchive = False
            note.save()
            response = {
                'success': True,
                'message': 'Notes isArchive successfully!'
            }
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong! Please try again...',
            }
            return Response(response)


class AllTrashNotesAPIView(generics.GenericAPIView):
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            trash = Notes.objects.filter(user_id=user.id, isTrash=True)
            serializer = TrashSerializer(trash, many=True)
            response = {
                "success": True,
                "msg": response_code[200],
                "data": serializer.data
            }
            return Response(response)
        except Exception:
            response = {
                "success": False,
                "msg": response_code[416],
            }
            return Response(response)


class TrashNotesAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwar):
        pk = self.kwargs.get('pk')
        note_id = pk
        note = Notes.objects.get(id=note_id)
        try:
            if not note.isTrash:
                note.isTrash = True
            else:
                note.isTrash = False
            note.save()
            response = {
                'success': True,
                'message': 'Notes isTrash successfully!'
            }
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong! Please try again...',
            }
            return Response(response)


class AllPinNotesAPIView(generics.GenericAPIView):
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            trash = Notes.objects.filter(user_id=user.id, isPinned=True)
            serializer = PinSerializer(trash, many=True)
            response = {
                "success": True,
                "msg": response_code[200],
                "data": serializer.data
            }
            return Response(response)
        except Exception:
            response = {
                "success": False,
                "msg": response_code[416],
            }
            return Response(response)


class PinNotesAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwar):
        pk = self.kwargs.get('pk')
        note_id = pk
        note = Notes.objects.get(id=note_id)
        try:
            if not note.isPinned:
                note.isPinned = True
            else:
                note.isPinned = False
            note.save()
            response = {
                'success': True,
                'message': 'Notes isPinned successfully!'
            }
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong! Please try again...',
            }
            return Response(response)


