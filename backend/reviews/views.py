from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count

from reviews.models import NormalizedRecord
from reviews.serializers import (
    NormalizedRecordSerializer
)

from audit.models import AuditLog


class RecordListAPIView(APIView):

    def get(self, request):

        records = NormalizedRecord.objects.all().order_by(
            '-created_at'
        )

        serializer = NormalizedRecordSerializer(
            records,
            many=True
        )

        return Response(serializer.data)


class DashboardStatsAPIView(APIView):

    def get(self, request):

        total_records = NormalizedRecord.objects.count()

        pending_records = NormalizedRecord.objects.filter(
            status='PENDING'
        ).count()

        approved_records = NormalizedRecord.objects.filter(
            status='APPROVED'
        ).count()

        suspicious_records = NormalizedRecord.objects.filter(
            status='SUSPICIOUS'
        ).count()

        rejected_records = NormalizedRecord.objects.filter(
            status='REJECTED'
        ).count()

        return Response({
            "total_records": total_records,
            "pending_records": pending_records,
            "approved_records": approved_records,
            "suspicious_records": suspicious_records,
            "rejected_records": rejected_records,
        })


class ApproveRecordAPIView(APIView):

    def post(self, request, record_id):

        try:

            record = NormalizedRecord.objects.get(
                id=record_id
            )

        except NormalizedRecord.DoesNotExist:

            return Response(
                {"error": "Record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        old_status = record.status

        record.status = "APPROVED"
        record.is_locked = True

        record.save()

        AuditLog.objects.create(
            record=record,
            action="APPROVED_RECORD",
            old_value={"status": old_status},
            new_value={"status": "APPROVED"},
            changed_by="Analyst"
        )

        return Response({
            "message": "Record approved successfully"
        })


class RejectRecordAPIView(APIView):

    def post(self, request, record_id):

        try:

            record = NormalizedRecord.objects.get(
                id=record_id
            )

        except NormalizedRecord.DoesNotExist:

            return Response(
                {"error": "Record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        old_status = record.status

        record.status = "REJECTED"

        record.save()

        AuditLog.objects.create(
            record=record,
            action="REJECTED_RECORD",
            old_value={"status": old_status},
            new_value={"status": "REJECTED"},
            changed_by="Analyst"
        )

        return Response({
            "message": "Record rejected successfully"
        })


class SuspiciousRecordsAPIView(APIView):

    def get(self, request):

        records = NormalizedRecord.objects.filter(
            status='SUSPICIOUS'
        )

        serializer = NormalizedRecordSerializer(
            records,
            many=True
        )

        return Response(serializer.data)