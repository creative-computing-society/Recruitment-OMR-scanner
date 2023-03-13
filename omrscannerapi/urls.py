from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.OMRScannerAPIView.as_view(), name="upload"),
    path('test/', views.index)
]