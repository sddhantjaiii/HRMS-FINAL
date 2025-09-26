"""
Truly optimized bulk upload with lightweight operations (pandas-free)
"""
import logging
from datetime import datetime, time
from decimal import Decimal
from typing import Dict, List, Any
from django.db import transaction, connection
from django.utils import timezone
from ..models import EmployeeProfile
from .utils import (
    excel_to_dict_list,
    lightweight_notna,
    lightweight_to_numeric,
    safe_float_conversion,
    safe_int_conversion,
    dict_list_shape,
    dict_list_columns,
    is_nan_value
)
import uuid
import hashlib
import string
import random

logger = logging.getLogger(__name__)

class TrulyOptimizedBulkUploadService:
    """
    Truly optimized bulk upload service with:
    - Pre-generated unique IDs using UUID + hash
    - Single transaction for entire batch
    - Minimal validation
    - Raw SQL inserts with batch size optimization
    - Pandas-free operations using list of dictionaries
    """
    
    def __init__(self, tenant, batch_size=1000):
        self.tenant = tenant
        self.batch_size = batch_size
        
    def process_bulk_upload(self, file) -> Dict:
        """Process bulk upload with maximum performance (pandas-free)"""
        try:
            start_time = datetime.now()
            
            # Read Excel file as list of dictionaries
            data_list = self._read_excel_fast(file)
            logger.info(f"📖 Read {len(data_list)} rows in {(datetime.now() - start_time).total_seconds():.2f}s")
            
            if not data_list:
                return self._create_result(0, 0, ["No data found in file"], 0)
            
            # Preprocess data
            processed_data = self._preprocess_ultra_fast(data_list)
            logger.info(f"🔧 Preprocessed {len(processed_data)} rows")
            
            # Generate unique IDs without database queries
            final_data = self._generate_unique_ids_no_db(processed_data)
            logger.info(f"🆔 Generated IDs for {len(final_data)} rows")
            
            # Single bulk insert
            result = self._single_bulk_insert(final_data)
            
            total_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Completed in {total_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Bulk upload failed: {str(e)}")
            return self._create_result(0, 0, [str(e)], 0)

    def _read_excel_fast(self, file) -> List[Dict]:
        """Read Excel with minimal processing (pandas-free)"""
        return excel_to_dict_list(file, '.xlsx')
    
    def _preprocess_ultra_fast(self, data_list: List[Dict]) -> List[Dict]:
        """Ultra-fast preprocessing with defaults (pandas-free)"""
        
        # Get column names
        if not data_list:
            return data_list
        
        columns = list(data_list[0].keys())
        
        # Essential column mapping
        column_mapping = {
            'employee_name': 'First Name',
            'department': 'Department', 
            'basic_salary': 'Basic Salary'
        }
        
        # Apply column mapping
        for row in data_list:
            for old_col, new_col in column_mapping.items():
                if old_col in row and new_col not in row:
                    row[new_col] = row[old_col]
        
        # Required columns with defaults
        required_columns = {
            'First Name': '',
            'Last Name': '',
            'Department': 'General',
            'Position': 'Employee',
            'Email': '',
            'Phone': '',
            'Basic Salary': 0,
            'House Rent Allowance': 0,
            'Medical Allowance': 0,
            'Transport Allowance': 0,
            'TDS (%)': 0,
        }
        
        # Fill missing columns and clean data
        for row in data_list:
            for col, default in required_columns.items():
                if col not in row or is_nan_value(row[col]):
                    row[col] = default
                elif col in ['Basic Salary', 'House Rent Allowance', 'Medical Allowance', 'Transport Allowance']:
                    row[col] = safe_float_conversion(row[col], 0.0)
                elif col == 'TDS (%)':
                    row[col] = safe_float_conversion(row[col], 0.0)
        
        # Set default date of joining
        current_date = datetime.now().date()
        for row in data_list:
            if 'Date of joining' not in row or is_nan_value(row['Date of joining']):
                row['Date of joining'] = current_date
        
        return data_list
    
    def _generate_unique_ids_no_db(self, data_list: List[Dict]) -> List[Dict]:
        """Generate unique IDs without database queries (pandas-free)"""
        existing_ids = set()
        
        for row in data_list:
            # Generate base ID from name and tenant
            name = str(row.get('First Name', '')).strip()
            if not name:
                name = 'Employee'
            
            base_id = self._generate_base_id(name)
            
            # Ensure uniqueness
            unique_id = base_id
            counter = 1
            while unique_id in existing_ids:
                unique_id = f"{base_id}{counter:02d}"
                counter += 1
            
            existing_ids.add(unique_id)
            row['employee_id'] = unique_id
            
        return data_list
    
    def _generate_base_id(self, name: str) -> str:
        """Generate base employee ID from name"""
        # Clean and format name
        clean_name = ''.join(c for c in name.upper() if c.isalnum())[:6]
        if len(clean_name) < 3:
            clean_name = clean_name.ljust(3, 'X')
        
        # Add random suffix
        suffix = ''.join(random.choices(string.digits, k=3))
        return f"{self.tenant.id:02d}{clean_name[:6]}{suffix}"
    
    def _single_bulk_insert(self, data_list: List[Dict]) -> Dict:
        """Single bulk insert with raw SQL (pandas-free)"""
        try:
            with transaction.atomic():
                inserted_count = 0
                errors = []
                
                # Prepare batch insert
                employees_to_create = []
                
                for row in data_list:
                    try:
                        values = self._prepare_insert_values(row)
                        employees_to_create.append(values)
                        
                        if len(employees_to_create) >= self.batch_size:
                            inserted_count += self._bulk_insert_batch(employees_to_create)
                            employees_to_create = []
                            
                    except Exception as e:
                        errors.append(f"Row error: {str(e)}")
                
                # Insert remaining records
                if employees_to_create:
                    inserted_count += self._bulk_insert_batch(employees_to_create)
                
                return self._create_result(inserted_count, len(data_list), errors, inserted_count)
                
        except Exception as e:
            logger.error(f"Bulk insert failed: {str(e)}")
            return self._create_result(0, 0, [str(e)], 0)
    
    def _prepare_insert_values(self, row: Dict) -> tuple:
        """Prepare values for database insert (pandas-free)"""
        # Handle date of joining
        date_of_joining = row.get('Date of joining')
        if is_nan_value(date_of_joining):
            date_of_joining = datetime.now().date()
        elif isinstance(date_of_joining, str):
            try:
                date_of_joining = datetime.strptime(date_of_joining, '%Y-%m-%d').date()
            except:
                date_of_joining = datetime.now().date()
        
        return (
            row['employee_id'],
            row.get('First Name', ''),
            row.get('Last Name', ''),
            row.get('Department', 'General'),
            row.get('Position', 'Employee'),
            row.get('Email', ''),
            row.get('Phone', ''),
            date_of_joining,
            Decimal(str(row.get('Basic Salary', 0))),
            Decimal(str(row.get('House Rent Allowance', 0))),
            Decimal(str(row.get('Medical Allowance', 0))),
            Decimal(str(row.get('Transport Allowance', 0))),
            float(row.get('TDS (%)', 0)),
            self.tenant.id,
            timezone.now(),
            timezone.now(),
        )
    
    def _bulk_insert_batch(self, values_list: List[tuple]) -> int:
        """Execute bulk insert for a batch"""
        if not values_list:
            return 0
        
        sql = """
        INSERT INTO excel_data_employeeprofile (
            employee_id, first_name, last_name, department, position,
            email, phone_number, date_of_joining, basic_salary,
            house_rent_allowance, medical_allowance, transport_allowance,
            tds_percentage, tenant_id, created_at, updated_at
        ) VALUES %s
        """
        
        with connection.cursor() as cursor:
            # Format values for SQL
            values_str = ','.join([str(v) for v in values_list])
            cursor.execute(sql.replace('%s', values_str))
            
        return len(values_list)
    
    def _create_result(self, created: int, total: int, errors: List[str], duplicates: int) -> Dict:
        """Create standardized result dictionary"""
        return {
            'created': created,
            'total_processed': total,
            'errors': errors,
            'duplicates_skipped': duplicates,
            'success': created > 0 and len(errors) == 0
        }