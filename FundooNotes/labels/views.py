from rest_framework import serializers, status
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# from .logger import get_logger
from labels.models import Labels

# Create your views here.
from rest_framework.views import APIView

from labels.serializers import LabelSerializer

# logger = get_logger()


class RetrieveAPIView(APIView):
    def get(self, request):
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


class CreateAPIView(APIView):
    def post(self, request):
        try:
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            labels = Labels(name=serializer.data.get('name'))
            labels.save()
            data = serializer.data
            data.update({'id': labels.id})
            response = {
                'success': True,
                'message': 'Labels created successfully!',
                'data': {'notes_list': data}
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'success': False,
                'message': 'Oops! Something went wrong!'
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class UpdateAPIView(APIView):
    def put(self, request, ):
        try:
            data = Labels.objects.get(pk=1)
            serializer = LabelSerializer(data, data=request.data)
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
            data = Labels.objects.get(pk=9)
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
