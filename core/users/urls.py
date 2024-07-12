from django.urls import path

from core.users.views import ProfileView, SolutionView, TopUsersListView

app_name = "users"

urlpatterns = [
    path("profile/", ProfileView.as_view()),
    path("solution/<int:id>/", SolutionView.as_view()),
    path("top-users/", TopUsersListView.as_view()),
]
