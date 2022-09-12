from django.urls import path
from . import views

urlpatterns = [
    path('', views.OMRScannerAPIView.as_view()),
]