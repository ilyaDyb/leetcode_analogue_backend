from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.core.cache import cache

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.auth_.models import User
from core.auth_.permissions import CustomIsAdminPermission, CustomIsAuthenticatedPermission
from core.main.models import Problem, Rate, SolutionResult, TestCase
from core.main.serializers import ProblemSerializer, TestCaseSerializer
from core.utils import CustomPagination


class ProblemListView(generics.ListAPIView):
    """
    List all problems
    """
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    pagination_class = CustomPagination
    # permission_classes = [CustomIsAuthenticatedPermission]

    # @swagger_auto_schema(
    #     operation_description="Get a list of all problems",
    #     responses={200: ProblemSerializer(many=True)}
    # )
    def get_quryset(self):
        cache_key = "all_problems"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        else:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            cache.set(cache_key, serializer.data, timeout=60*15)
            return Response(serializer.data)


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
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        operation_description="Retrieve a problem by ID",
        responses={200: ProblemSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        operation_description="Update a problem by ID",
        request_body=ProblemSerializer,
        responses={200: ProblemSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        operation_description="Partial update a problem by ID",
        request_body=ProblemSerializer,
        responses={200: ProblemSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
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
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        operation_description="Create a new problem",
        request_body=ProblemSerializer,
        responses={201: ProblemSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class TestCaseView(generics.CreateAPIView):
    """
    Create testcase
    """
    permission_classes = [CustomIsAdminPermission]
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

    
    def perform_create(self, serializer):
        id_problem = self.kwargs.get("id")
        serializer.save(problem_id=id_problem)


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'input_data': openapi.Schema(type=openapi.TYPE_STRING, description='Input data for the test case', example="[1,2,3]"),
                'expected_output': openapi.Schema(type=openapi.TYPE_STRING, description='Expected output for the test case', example="[1,4,9]"),
            },
            required=['input_data', 'expected_output']
        ),
        responses={201: TestCaseSerializer()},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        return Response(serializer.data, status=201)


class TestCasesListView(generics.ListAPIView):
    """
    Get testcases of problem by id
    """
    permission_classes = [CustomIsAuthenticatedPermission]
    serializer_class = TestCaseSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('not_full', openapi.IN_QUERY, description="Not full list with 3 obj full list", type=openapi.TYPE_BOOLEAN),
        ],
        operation_description="Get a list of test cases for a specific problem",
        responses={200: TestCaseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        id_problem = self.kwargs["id"]
        not_full = request.query_params.get("not_full")

        if not_full:
            queryset = TestCase.objects.filter(problem_id=id_problem)[:3]
        else:
            queryset = TestCase.objects.filter(problem_id=id_problem)

        serializater = self.get_serializer(queryset, many=True)

        return Response(serializater.data)
    

class LikeProblemView(APIView):
    """
    Url for liking problems
    """
    permission_classes = [CustomIsAuthenticatedPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        operation_description="Like a problem",
        responses={
            200: "OK",
            201: "Created",
            205: "Reset Content",
            404: "Not Found",
            400: "Bad Request",
        }
    )
    def post(self, request, problem_id, user_id):
        try:
            problem = Problem.objects.get(pk=problem_id)
            user = User.objects.get(pk=user_id)
        except (Problem.DoesNotExist, User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if not SolutionResult.objects.filter(problem=problem, user=user).exists():
            return Response({"error": "You need to solve this problem to decide whether you like it or not"}, status=status.HTTP_400_BAD_REQUEST)
        
        rate, created = Rate.objects.get_or_create(user=user, problem=problem)
        
        if created or rate.rate_type != Rate.LIKE:
            rate.rate_type = Rate.LIKE
            rate.save()
            if not created:
                return Response(status=status.HTTP_205_RESET_CONTENT)
            return Response(status=status.HTTP_201_CREATED)
        else:
            rate.delete()
            return Response(status=status.HTTP_200_OK)


class DislikeProblemView(APIView):
    """
    Url for disliking problems
    """
    permission_classes = [CustomIsAuthenticatedPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        operation_description="Dislike a problem",
        responses={
            200: "OK",
            201: "Created",
            205: "Reset Content",
            404: "Not Found",
            400: "Bad Request",
        }
    )
    def post(self, request, problem_id, user_id):
        try:
            problem = Problem.objects.get(pk=problem_id)
            user = User.objects.get(pk=user_id)
        except (Problem.DoesNotExist, User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not SolutionResult.objects.filter(problem=problem, user=user).exists():
            return Response({"error": "You need to solve this problem to decide whether you like it or not"}, status=status.HTTP_400_BAD_REQUEST)

        rate, created = Rate.objects.get_or_create(user=user, problem=problem)

        if created or rate.rate_type != Rate.DISLIKE:
            rate.rate_type = Rate.DISLIKE
            rate.save()
            if not created:
                return Response(status=status.HTTP_205_RESET_CONTENT)
            return Response(status=status.HTTP_201_CREATED)
        else:
            rate.delete()
            return Response(status=status.HTTP_200_OK)
