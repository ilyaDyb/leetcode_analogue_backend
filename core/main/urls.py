from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('test/', views.test_view, name='test'),
    path('test-view/', views.TestApiView.as_view(), name='testviw'),
]