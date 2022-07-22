from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from users.models import User
from .logger import get_logger
from .models import Notes
from Fundoonotes.exceptions import DoesNotExist
from rest_framework.views import APIView
from .serializers import NotesSerializer, TrashSerializer, PinSerializer
from Fundoonotes.Response import response_code
from .utils import NoteRedis

logger = get_logger()
Redis = settings.CACHES


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
        user_id = request.user.id
        user = request.user
        try:
            serializer = NotesSerializer(data=request.data, partial=True)
            serializer.is_valid()
            serializer.save(user_id=user.id)
            NoteRedis.save(key=user_id, value=serializer.data)
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
                'data': str(e)
            }
            logger.exception(str(e))
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416],
                'data': str(e)}
            logger.exception(str(e))
            return Response(response)


class RetrieveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if user:
                data = NoteRedis.extract(key=user.id)
                print(data)
                # data3 = [(k, data[k]) for k in data]
                # print(data3)
                # notes = Notes.objects.filter(user=request.user, isTrash=False, isArchive=False)
                # serializer = GetNoteSerializer(notes, many=True)
                # logger.info('Getting the notes data on %s', timezone.now())
                # serialized_data = serializer.data
                # for note in serialized_data:
                #     NoteRedis.save(key=user.id,value=note)
                response = {
                    'success': True,
                    'message': response_code[200],
                    'data': data,
                }
                logger.info('successfully get Notes from database')
                return Response(response)

        except DoesNotExist as e:
            response = {
                'success': False,
                'message': response_code[307],
                'data': str(e)
            }
            logger.exception(e)
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416],
                'data': str(e)
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotesSerializer
    data = Notes.objects.all()

    def get_objects(self, pk, user_id):
        try:
            return Notes.objects.get(pk=pk, user_id=user_id)
        except Exception:
            response = {
                'success': False,
                'message': response_code[416],
            }
            return Response(response)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user_id = self.kwargs.get('user_id')
        note = self.get_objects(pk=pk, user_id=user_id)
        serializer = NotesSerializer(note)
        response = {
            'success': True,
            'message': response_code[200],
            'data': serializer.data
        }
        return Response(response)

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user_id = self.kwargs.get('user_id')
        note = self.get_objects(pk=pk, user_id=user_id)
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
        logger.exception(response_code[416])
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
            logger.exception(response_code[416])
            return Response(response)


class ArchiveNotesAPIView(generics.GenericAPIView):
    serializer_class = NotesSerializer

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
                "success": False,
                "msg": response_code[416],
            }
            logger.exception(response_code[416])
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
            logger.exception(response_code[416])
            return Response(response)


class TrashNotesAPIView(generics.GenericAPIView):
    serializer_class = NotesSerializer

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
                "success": False,
                "msg": response_code[416],
            }
            logger.exception(response_code[416])
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
            logger.exception(response_code[416])
            return Response(response)


class PinNotesAPIView(generics.GenericAPIView):
    serializer_class = NotesSerializer

    def put(self, request, *args, **kwar):
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
            logger.exception(response_code[416])
            return Response(response)


class DisplayNoteByLabelView(generics.GenericAPIView):
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()

    def get(self, request, label):
        notes = Notes.objects.filter(user_id=request.user.id, isTrash=False, label__contains=[str(label)])
        if notes.count() == 0:
            response=({'code': 409, 'msg': response_code[409]})
            return Response(response)
        serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data, status=200)


class CollaboratedNoteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()

    def get(self, request):
        notes = Notes.objects.filter(collaborator__in=[request.user.id], isTrash=False, isArchive=False)
        if notes.count() == 0:
            response = {
                'success': False,
                'msg': response_code[409]
            }
            return Response(response)
        serializer = NotesSerializer(notes, many=True)
        response = {
            'success': True,
            'msg': response_code[200],
            'data': serializer.data
        }
        return Response(response)


class LabelNoteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()

    def get(self, request):
        notes = Notes.objects.filter(label__in=[request.user.id], isTrash=False, isArchive=False)
        if notes.count() == 0:
            return Response({'code': 409, 'msg': response_code[409]})
        serializer = NotesSerializer(notes, many=True)
        return Response({"data": serializer.data, "code": 200, "msg": response_code[200]})


# from datetime import datetime
# from .exceptions import PassedTimeException
#
#
# def validate_time(time_data):
#     now = datetime.now()
#     current_time = now.strftime("%H:%M")
#     if time_data < current_time:
#         raise PassedTimeException


# class CreateAPIView1(generics.GenericAPIView):
#     serializer_class = NotesSerializer
#     queryset = Notes.objects.all()
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request):
#         data = request.data
#         user_id = request.user.id
#         user = request.user
#         try:
#             serializer = NotesSerializer1(data=data, partial=True)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save(user_id=user.id)
#                 reminder = request.data['reminder']
#
#                 data = serializer.data
#                 print(data)
#                 return Response(data, status=status.HTTP_201_CREATED)
#             return Response(status.HTTP_400_BAD_REQUEST)
#
#         except ValidationError as e:
#             response = {
#                 'success': False,
#                 'message': response_code[308],
#                 'data': str(e)
#             }
#             logger.exception(str(e))
#             return Response(response)
#         except Exception as e:
#             response = {
#                 'success': False,
#                 'message': response_code[416],
#                 'data': str(e)}
#             logger.exception(str(e))
#             return Response(response)
