from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class TestAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({"status": "successfully"}, status=200)