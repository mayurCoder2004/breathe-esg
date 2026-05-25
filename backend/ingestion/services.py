import pandas as pd

from ingestion.models import DataSource, RawData
from reviews.models import NormalizedRecord
from companies.models import Company


class CSVIngestionService:

    @staticmethod
    def process_file(company_id, source_type, uploaded_file):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist as exc:
            raise ValueError(
                f"Company with id={company_id} does not exist."
            ) from exc

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

            try:
                normalized_data = CSVIngestionService.normalize_row(
                    source_type,
                    raw_json
                )
            except KeyError as exc:
                missing_column = str(exc).strip("'")
                raise ValueError(
                    f"Invalid CSV format for {source_type}. "
                    f"Missing column: {missing_column} (row {index + 1})."
                ) from exc

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
            required_columns = ["MENGE", "MEINS"]
            for column in required_columns:
                if column not in row:
                    raise KeyError(column)

            return {
                "category": "Fuel",
                "scope": "Scope 1",
                "amount": float(row["MENGE"]),
                "unit": row["MEINS"]
            }

        elif source_type == "UTILITY":
            required_columns = ["Usage_kWh"]
            for column in required_columns:
                if column not in row:
                    raise KeyError(column)

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

        raise ValueError(
            f"Unsupported source type: {source_type}"
        )

    @staticmethod
    def validate_row(data):

        if data["amount"] < 0:
            return "REJECTED"

        if data["amount"] > 100000:
            return "SUSPICIOUS"

        return "PENDING"
