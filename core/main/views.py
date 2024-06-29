from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.auth_.permissions import CustomIsAdminPermission, CustomIsAuthenticatedPermission
from core.main.models import Problem
from core.main.serializers import ProblemSerializer


class ProblemListView(generics.ListAPIView):
    """
    List all problems
    """
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    @swagger_auto_schema(
        operation_description="Get a list of all problems",
        responses={200: ProblemSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProblemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a problem instance
    """
    permission_classes = [CustomIsAuthenticatedPermission]
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    lookup_field = "id"

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING),
        ],
        operation_description="Retrieve a problem by ID",
        responses={200: ProblemSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING),
        ],
        operation_description="Update a problem by ID",
        request_body=ProblemSerializer,
        responses={200: ProblemSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING),
        ],
        operation_description="Partial update a problem by ID",
        request_body=ProblemSerializer,
        responses={200: ProblemSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING),
        ],
        operation_description="Delete a problem by ID",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProblemCreateView(generics.CreateAPIView):
    """
    Create a new problem
    """
    permission_classes = [CustomIsAdminPermission]
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING),
        ],
        operation_description="Create a new problem",
        request_body=ProblemSerializer,
        responses={201: ProblemSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)