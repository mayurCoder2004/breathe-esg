from django.db import models
from companies.models import Company
from ingestion.models import DataSource


class NormalizedRecord(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED'),
        ('SUSPICIOUS', 'SUSPICIOUS'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    data_source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE
    )

    category = models.CharField(max_length=100)

    scope = models.CharField(max_length=50)

    activity_amount = models.FloatField()

    unit = models.CharField(max_length=50)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    is_locked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.activity_amount}"