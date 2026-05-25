from django.urls import path

from reviews.views import (
    RecordListAPIView,
    DashboardStatsAPIView,
    ApproveRecordAPIView,
    RejectRecordAPIView,
    SuspiciousRecordsAPIView,
)

urlpatterns = [

    path(
        'records/',
        RecordListAPIView.as_view(),
        name='record-list'
    ),

    path(
        'dashboard/stats/',
        DashboardStatsAPIView.as_view(),
        name='dashboard-stats'
    ),

    path(
        'records/<int:record_id>/approve/',
        ApproveRecordAPIView.as_view(),
        name='approve-record'
    ),

    path(
        'records/<int:record_id>/reject/',
        RejectRecordAPIView.as_view(),
        name='reject-record'
    ),

    path(
        'records/suspicious/',
        SuspiciousRecordsAPIView.as_view(),
        name='suspicious-records'
    ),
]