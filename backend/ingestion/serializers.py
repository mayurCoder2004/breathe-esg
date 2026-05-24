from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):

    company_id = serializers.IntegerField()

    source_type = serializers.ChoiceField(
        choices=['SAP', 'UTILITY', 'TRAVEL']
    )

    file = serializers.FileField()