import pandas as pd

from ingestion.models import DataSource, RawData
from reviews.models import NormalizedRecord
from companies.models import Company


class CSVIngestionService:

    @staticmethod
    def process_file(company_id, source_type, uploaded_file):

        company = Company.objects.get(id=company_id)

        data_source = DataSource.objects.create(
            company=company,
            source_type=source_type,
            file_name=uploaded_file.name,
            uploaded_by="Admin"
        )

        df = pd.read_csv(uploaded_file)

        for index, row in df.iterrows():

            raw_json = row.to_dict()

            RawData.objects.create(
                data_source=data_source,
                raw_json=raw_json,
                row_number=index + 1
            )

            normalized_data = CSVIngestionService.normalize_row(
                source_type,
                raw_json
            )

            status = CSVIngestionService.validate_row(
                normalized_data
            )

            NormalizedRecord.objects.create(
                company=company,
                data_source=data_source,
                category=normalized_data["category"],
                scope=normalized_data["scope"],
                activity_amount=normalized_data["amount"],
                unit=normalized_data["unit"],
                status=status
            )

        return data_source

    @staticmethod
    def normalize_row(source_type, row):

        if source_type == "SAP":

            return {
                "category": "Fuel",
                "scope": "Scope 1",
                "amount": float(row["MENGE"]),
                "unit": row["MEINS"]
            }

        elif source_type == "UTILITY":

            return {
                "category": "Electricity",
                "scope": "Scope 2",
                "amount": float(row["Usage_kWh"]),
                "unit": "kWh"
            }

        elif source_type == "TRAVEL":

            return {
                "category": "Business Travel",
                "scope": "Scope 3",
                "amount": 1,
                "unit": "trip"
            }

    @staticmethod
    def validate_row(data):

        if data["amount"] < 0:
            return "REJECTED"

        if data["amount"] > 100000:
            return "SUSPICIOUS"

        return "PENDING"