from django.urls import path

from core.api import views

app_name = "api"

urlpatterns = [
    path("test/", views.TestAPIView.as_view(), name="test")
]
