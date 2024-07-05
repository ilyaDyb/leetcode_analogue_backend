
from django.urls import path
from .views import RunCodeView, SubmitCodeView, ReceiveResultView

app_name = "code_interpreter"

urlpatterns = [
    path("run-code/<int:id_problem>", RunCodeView.as_view()),
    path("submit-code/<int:id_problem>", SubmitCodeView.as_view()),
    path("receive_result/", ReceiveResultView.as_view()),
]
