import os
from django.conf import settings
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    from excel_data.utils.utils import excel_to_dict_list
from django.core.management.base import BaseCommand
from excel_data.models import SalaryData  # Adjust to your actual model

class Command(BaseCommand):
    help = 'Import salary data from Excel'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'import_files', 'updated.xlsx')
        
        if HAS_PANDAS:
            df = pd.read_excel(file_path)
            data_list = df.to_dict('records')
        else:
            with open(file_path, 'rb') as f:
                data_list = excel_to_dict_list(f, '.xlsx')

        for row in data_list:
            SalaryData.objects.update_or_create(
                name=row.get('NAME', ''),
                defaults={
                    'basic_salary': row.get('SALARY', 0),
                    'days_absent': row.get('ABSENT', 0),
                    'days_present': row.get('DAYS', 0),
                    'ot_hours': row.get('OT', 0),
                    'ot_charges': row.get('OT CHARGES', 0),
                    'late_minutes': row.get('LATE', 0),
                    'late_charges': row.get('CHARGE', 0),
                    'salary_wo_advance_deduction': row.get('SAL+OT', 0),
                    'adv_paid_on_25th': row['ADVANCE'],
                    'repayment_of_old_adv': row['OLD ADV'],
                    'net_payable': row['NETT SALRY'],
                    'total_old_advance': row['TOTAL OLD ADVANCE'],
                    'final_balance_advance': row['BALANCE ADVANCE'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))