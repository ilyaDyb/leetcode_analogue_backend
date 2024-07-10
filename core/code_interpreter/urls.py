from django.urls import path
from .views import (
    RunCodeView,
    SubmitCodeView,
    TaskStatusView,
    SaveSolutionResultView,
)

app_name = "code_interpreter"

urlpatterns = [
    path("run-code/<int:id_problem>/", RunCodeView.as_view()),
    path("submit-code/<int:id_problem>/", SubmitCodeView.as_view()),
    path("task-status/<str:task_id>/", TaskStatusView.as_view()),
    path("save-solution/", SaveSolutionResultView.as_view()),
]
