from django.apps import AppConfig


class ExcelDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'excel_data'

    def ready(self):
        try:
            import excel_data.signals
        except ImportError as e:
            # Skip signals import if there are issues (for deployment debugging)
            import os
            if os.environ.get('DJANGO_USE_LIGHTWEIGHT') == 'true':
                pass  # Skip signals in lightweight mode
            else:
                raise e
