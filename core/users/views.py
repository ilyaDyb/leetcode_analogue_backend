from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.auth_.permissions import CustomIsAuthenticatedPermission
from core.code_interpreter.serializers import SolutionResultSerializer
from core.main.models import SolutionResult
from core.users.serializers import UserProfileSerializer

class ProfileView(APIView):
    """
    Url for getting user's profile
    """
    permission_classes = [CustomIsAuthenticatedPermission]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(instance=user)
        return Response(serializer.data)
    
class SolutionView(generics.RetrieveAPIView):
    """
    recieve problem id and send details for solution
    """
    permission_classes = [CustomIsAuthenticatedPermission]
    serializer_class = SolutionResultSerializer
    queryset = SolutionResult.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING),
        ],
        operation_description="Retrieve a problem by ID",
        responses={200: SolutionResultSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
