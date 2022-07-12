from rest_framework import serializers, status, generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from Fundoonotes.Response import response_code
from labels.models import Labels
from labels.serializers import LabelSerializer


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
            }
            return Response(response)
        except Exception as e:
            response = {
                'success': False,
                'message': response_code[416],
            }
            return Response(response)

    def get(self, request):
        user = request.user
        try:
            data = Labels.objects.all()
            serializer = LabelSerializer(data, many=True)
            serialized_data = serializer.data
            response = {
                'status': 'Successfully Retrieved all Data',
                'user': serialized_data,
                'message': 'Getting Labels successfully!',
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong! Please try again...'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
