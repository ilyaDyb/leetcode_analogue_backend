from django.urls import path
from .views import ProblemsListView, ProblemView

app_name = "main"

urlpatterns = [
    path('problems/', ProblemsListView.as_view(), name='problems'),
    path('problem/', ProblemView.as_view(), name='problem'),
]