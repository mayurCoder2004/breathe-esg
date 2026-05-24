from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ingestion.serializers import FileUploadSerializer
from ingestion.services import CSVIngestionService


class FileUploadAPIView(APIView):

    def post(self, request):

        serializer = FileUploadSerializer(
            data=request.data
        )

        if serializer.is_valid():

            CSVIngestionService.process_file(
                company_id=serializer.validated_data["company_id"],
                source_type=serializer.validated_data["source_type"],
                uploaded_file=serializer.validated_data["file"]
            )

            return Response(
                {"message": "File uploaded successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )