from django.urls import path

from .views import (
    MyTokenObtaionPairView,
    RegisterView,
    LogoutView,
    LoginView,
)

from rest_framework_simplejwt.views import TokenRefreshView


app_name = "users"

urlpatterns = [
    path("user/token/", MyTokenObtaionPairView.as_view(), name="token_obtain_pair"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/register/", RegisterView.as_view()),
    path("user/login/", LoginView.as_view()),
    path("user/logout/", LogoutView.as_view()),
]