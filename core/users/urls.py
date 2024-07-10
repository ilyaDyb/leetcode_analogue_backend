from django.urls import path

from core.users.views import ProfileView, SolutionView

app_name = "users"

urlpatterns = [
    path("profile/", ProfileView.as_view()),
    path("solution/<int:id>/", SolutionView.as_view()),
]
