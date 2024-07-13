from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.auth_.models import User
from core.auth_.permissions import CustomIsAuthenticatedPermission
from core.code_interpreter.serializers import SolutionResultSerializer
from core.main.models import SolutionResult
from core.users.serializers import TopUserSerializer, UserProfileSerializer
from core.utils import CustomPagination

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
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        operation_description="Retrieve a problem by ID",
        responses={200: SolutionResultSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TopUsersListView(generics.ListAPIView):
    """
    Url which return top users list
    """
    permission_classes = [CustomIsAuthenticatedPermission]
    serializer_class = TopUserSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of results to return per page", type=openapi.TYPE_INTEGER),
        ],
        operation_description="Retrieve a list of top users with their positions in the ranking."
    )
    def get_queryset(self):
        top_users = User.objects.annotate(solved_problems=Count("results")).order_by("-solved_problems")
        ranked_users = [
            {"position": index + 1, "user_id": user.id, "username": user.username, "solved_problems": user.solved_problems}
            for index, user in enumerate(top_users)
        ]
        return ranked_users