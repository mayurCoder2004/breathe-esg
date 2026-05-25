from rest_framework import serializers

from reviews.models import NormalizedRecord


class NormalizedRecordSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source='company.name',
        read_only=True
    )

    source_type = serializers.CharField(
        source='data_source.source_type',
        read_only=True
    )

    class Meta:
        model = NormalizedRecord

        fields = [
            'id',
            'company_name',
            'source_type',
            'category',
            'scope',
            'activity_amount',
            'unit',
            'status',
            'is_locked',
            'created_at',
        ]