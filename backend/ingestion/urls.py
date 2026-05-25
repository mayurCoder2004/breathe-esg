from django.urls import path

from ingestion.views import FileUploadAPIView

urlpatterns = [
    path(
        'upload/',
        FileUploadAPIView.as_view(),
        name='file-upload'
    ),
]