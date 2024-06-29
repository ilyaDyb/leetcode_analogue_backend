from django.urls import path
from .views import ProblemListView, ProblemRetrieveUpdateDestroyView, ProblemCreateView

app_name = "main"

urlpatterns = [
    path('problems/', ProblemListView.as_view(), name='problems'),
    path('problem/<int:id>/', ProblemRetrieveUpdateDestroyView.as_view(), name='problem'),
    path('problem/', ProblemCreateView.as_view(), name='problem'),
]