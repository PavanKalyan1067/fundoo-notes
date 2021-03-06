from rest_framework import status, generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from Fundoonotes import logger
from Fundoonotes.Response import response_code
from labels.models import Labels
from labels.serializers import LabelSerializer

'''
class LabelAPIView(generics.GenericAPIView):class has 2 methods
    1. def get(self, request):  
        get method will fetch all the label for logged in user. And display it.
    2. def post(self, request):
        post method will be responsible for create label and save it into database. Serializer will be responsible for
        validation and serialize the data.
'''


class LabelAPIView(generics.GenericAPIView):
    serializer_class = LabelSerializer
    queryset = Labels.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            serializer = LabelSerializer(data=request.data, partial=True)
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
                'data': str(e)
            }
            logger.exception(str(e))
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416],
                'data': str(e)
            }
            logger.exception(str(e))
            return Response(response)

    def get(self, request):
        user = request.user
        try:
            data = Labels.objects.all()
            serializer = LabelSerializer(data, many=True)
            serialized_data = serializer.data
            response = {
                'status': True,
                'message': 'Getting Labels successfully!',
                'data': serialized_data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong! Please try again...',
                'data': str(e)
            }
            logger.exception(str(e))
            return Response(response)


'''
class UpdateLabelsAPIView(generics.GenericAPIView):
    def get_objects(self, pk):
        get_objects method will fetch single label object by unique id. If object is not there it will raise DoesNotExistException
    def get(self, request, *args, **kwargs):
        get method will display single label object according to serializer field.
    def put(self, request, *args, **kwargs):
        put method is responsible for update any single label object witch is fetched by get method.
'''


class UpdateLabelsAPIView(generics.GenericAPIView):
    serializer_class = LabelSerializer
    data = Labels.objects.all()

    def get_objects(self, pk):
        try:
            return Labels.objects.get(pk=pk)
        except Exception:
            response = {
                'success': False,
                'message': response_code[416],
            }
            return Response(response)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        note = self.get_objects(pk=pk)
        serializer = LabelSerializer(note)
        response = {
            'success': True,
            'message': response_code[200],
            'data': serializer.data
        }
        return Response(response)

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        note = self.get_objects(pk=pk)
        try:
            serializer = LabelSerializer(note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                note = Labels.objects.get(pk=pk)
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
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong! Please try again...',
                'data': str(e)
            }
            logger.exception(str(e))
            return Response(response)


'''class DeleteAPIView(generics.GenericAPIView):
    def delete(self, request, pk):
        delete method is responsible to delete any single label object witch is fetched by get method.
'''


class DeleteAPIView(generics.GenericAPIView):
    def delete(self, request, pk):
        try:
            data = Labels.objects.get(pk=pk)
            data.delete()
            response = {
                'status': True,
                'message': 'Successfully Deleted Data',
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong! Please try again...',
                'data': str(e)
            }
            logger.exception(str(e))
            return Response(response)
