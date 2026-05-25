from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'companies'

    def ready(self):

        try:
            from companies.models import Company

            if not Company.objects.filter(
                name="Infosys"
            ).exists():

                Company.objects.create(
                    name="Infosys",
                    industry="IT"
                )

        except Exception:
            pass