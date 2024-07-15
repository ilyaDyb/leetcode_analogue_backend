from django.urls import path
from .views import (
    DislikeProblemView,
    LikeProblemView,
    ProblemListView,
    ProblemRetrieveUpdateDestroyView,
    ProblemCreateView,
    TestCaseView,
    TestCasesListView,
    LoadTestCasesView,
)

app_name = "main"

urlpatterns = [
    path("problems/", ProblemListView.as_view(), name="problems"),
    path("problem/<int:id>/", ProblemRetrieveUpdateDestroyView.as_view(), name="problem"),
    path("problem/", ProblemCreateView.as_view(), name="problem"),

    path("problem/<int:id>/testcase/", TestCaseView.as_view(), name="testcase_create"),
    path("problem/<int:id>/testcases/", TestCasesListView.as_view(), name="testcases"),
    path("problem/<int:id>/load-testcases/", LoadTestCasesView.as_view(), name="load_testcases"),

    path("problem/<int:problem_id>/like/<int:user_id>/", LikeProblemView.as_view()),
    path("problem/<int:problem_id>/dislike/<int:user_id>/", DislikeProblemView.as_view()),
]
