import json

from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.core import serializers

from celery.result import AsyncResult

from core.auth_.permissions import CustomIsAuthenticatedPermission
from core.code_interpreter.serializers import SolutionResultSerializer
from core.executor.tasks import run_user_code
from core.main.models import TestCase

from .proccessing_json import proccess_result

class RunCodeView(APIView):
    """  
    Runs the code with three test cases. Shows but does not save results and statistics,
    but displays errors if there are any, and also whether these test cases passed or not.
    """
    permission_classes = [CustomIsAuthenticatedPermission]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING, example='string'),
            },
            required=['code']
        ),
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        # responses={200: ProblemSerializer()}
    )
    def post(self, request, id_problem):
        user_code = request.data.get('code')
        try:
            testcases = serializers.serialize('json', TestCase.objects.filter(problem_id=id_problem)[:3])
        except Exception:
            return Response({"No problem with such id"})
        task = run_user_code.delay(str(request.user.id), user_code, json.loads(testcases))

        return Response({"task_id": task.id})



class SubmitCodeView(APIView):
    """  
    Runs the code with all test cases. Shows and saves results, as well as statistics,
    displays errors, if any, and the number of passed test cases.
    And if everything is successful, then execution statistics: execution time and RAM
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING, example='string'),
            },
            required=['code']
        ),
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        # responses={200: ProblemSerializer()}
    )
    def post(self, request, id_problem):
        user_code = request.data.get('code')
        try:
            testcases = serializers.serialize('json', TestCase.objects.filter(problem_id=id_problem))
        except Exception:
            return Response({"No problem with such id"})
        task = run_user_code.delay(str(request.user.id), user_code, json.loads(testcases))

        return Response({"task_id": task.id})
    

class ReceiveResultView(APIView):
    def post(self, request):
        result = request.data.get('result')
        # Here you can handle the result (e.g., save to database)
        print(f"Received result: {result}")
        return Response({"detail": "Result received"})
    

class TaskStatusView(APIView):
    """
    Url for checking result user's code
    """
    permission_classes = [CustomIsAuthenticatedPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
    )
    def get(self, request, task_id, *args, **kwargs):
        task = AsyncResult(task_id)

        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'result': 'Task is still pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'result': task.result
            }
        else:
            response = {
                'state': task.state,
                'result': str(task.info),
            }
        if response["state"] == "SUCCESS":
            result = response["result"]
            json_result = proccess_result(result)
            response["result"] = json_result
        return Response(response)
    

class SaveSolutionResultView(APIView):
    """
    View to save solution results.
    """
    permission_classes = [CustomIsAuthenticatedPermission]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        operation_description="Create a new problem",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'problem': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                'user': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                'lead_time': openapi.Schema(type=openapi.TYPE_INTEGER, example=22),
                'memory_used': openapi.Schema(type=openapi.TYPE_STRING, example="20.40"),
                'user_code': openapi.Schema(type=openapi.TYPE_STRING, example="def solution(lst): return [x**2 for x in lst]"),
                'passed': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            },
        ),
        responses={201: SolutionResultSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = SolutionResultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)