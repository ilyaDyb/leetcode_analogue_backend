from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema



@api_view(['GET'])
def test_view(request):
    return Response({"message": "Hello from main app"})


class TestApiView(APIView):
    def post(self, request, *args, **kwargs):
        return Response({"message": "test message"})
    def get(self, request, *args, **kwargs):
        return Response({"message": "test message"})