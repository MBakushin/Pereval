from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .serializers import *


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImagesViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PerevalViewset(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filterset_fields = ('user__email',)

    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': None,
                'id': serializer.data['id'],
            })
        elif status.HTTP_400_BAD_REQUEST:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "Bad request",
                'id': None
            })
        elif status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': "Internal server error",
                'id': None
            })

    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status == 'NW':
            serializer = PerevalSerializer(pereval, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'state': '1',
                    'status': status.HTTP_200_OK,
                    'message': "Changes were saved successfully",
                    'id': serializer.data['id']
                })
            if status.HTTP_400_BAD_REQUEST:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': "Bad request",
                    'id': None
                })
            if status.HTTP_500_INTERNAL_SERVER_ERROR:
                return Response({
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': "Internal server error",
                    'id': None
                })
        else:
            return Response({
                'state': '0',
                'message': f"Rejected, pereval status: {pereval.status}",
                'id': None
            })

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        pass
