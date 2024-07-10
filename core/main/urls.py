from django.urls import path
from .views import (
    ProblemListView,
    ProblemRetrieveUpdateDestroyView,
    ProblemCreateView,
    TestCaseView,
    TestCasesListView,
)

app_name = "main"

urlpatterns = [
    path("problems/", ProblemListView.as_view(), name="problems"),
    path("problem/<int:id>/", ProblemRetrieveUpdateDestroyView.as_view(), name="problem"),
    path("problem/", ProblemCreateView.as_view(), name="problem"),
    path("problem/<int:id>/testcase/", TestCaseView.as_view(), name="testcase_create"),
    path("problem/<int:id>/testcases/", TestCasesListView.as_view(), name="testcases"),
]
