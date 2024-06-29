from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema



class ProblemsListView(generics.ListAPIView):
    ...


class ProblemView(APIView):
    ...

