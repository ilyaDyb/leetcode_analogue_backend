import json
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.core import serializers

from core.auth_.permissions import CustomIsAuthenticatedPermission
from core.executor.tasks import run_user_code
from core.main.models import TestCase

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
            testcases = serializers.serialize('json', TestCase.objects.filter(problem_id=id_problem))
        except Exception:
            return Response({"No problem with such id"})
        run_user_code.delay(str(request.user.id), user_code, json.loads(testcases))
        return Response({"detail": f"type: {type(json.loads(testcases))} : {json.loads(testcases)}"})



class SubmitCodeView(APIView):
    """  
    Runs the code with all test cases. Shows and saves results, as well as statistics,
    displays errors, if any, and the number of passed test cases.
    And if everything is successful, then execution statistics: execution time and RAM
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
    def post(self, id_problem):
        return Response({})
    

class ReceiveResultView(APIView):
    def post(self, request):
        result = request.data.get('result')
        # Here you can handle the result (e.g., save to database)
        print(f"Received result: {result}")
        return Response({"detail": "Result received"})