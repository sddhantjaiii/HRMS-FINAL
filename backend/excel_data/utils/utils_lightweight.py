import threading
import math
from decimal import Decimal, InvalidOperation

# Thread local storage for current tenant
_thread_local = threading.local()

def set_current_tenant(tenant):
    """Set the current tenant in thread local storage"""
    _thread_local.tenant = tenant

def get_current_tenant():
    """Get the current tenant from thread local storage"""
    return getattr(_thread_local, 'tenant', None)

def clear_current_tenant():
    """Clear the current tenant from thread local storage"""
    if hasattr(_thread_local, 'tenant'):
        delattr(_thread_local, 'tenant')

def generate_employee_id(name: str, tenant_id: int, department: str = None) -> str:
    """
    Generate employee ID using format: First three letters-Department first two letters-Tenant id
    Example: Siddhant Marketing Analysis tenant_id 025 -> SID-MA-025
    
    In case of collision with same name, add postfix A, B, C
    Example: SID-MA-025-A, SID-MA-025-B, SID-MA-025-C
    """
    from ..models import EmployeeProfile
    import uuid

    # Clean and format the name
    clean_name = ''.join(c for c in name if c.isalpha())
    if len(clean_name) >= 3:
        name_part = clean_name[:3].upper()
    else:
        name_part = clean_name.upper().ljust(3, 'X')

    # Format tenant ID with leading zeros
    tenant_part = str(tenant_id).zfill(3)

    # Handle department
    if department:
        clean_dept = ''.join(c for c in department if c.isalpha())
        if len(clean_dept) >= 2:
            dept_part = clean_dept[:2].upper()
        else:
            dept_part = clean_dept.upper().ljust(2, 'X')
    else:
        dept_part = 'GE'  # General

    # Create base employee ID
    base_id = f"{name_part}-{dept_part}-{tenant_part}"

    # Check for existing employee IDs and handle collisions
    tenant = get_current_tenant()
    existing_ids = EmployeeProfile.objects.filter(
        tenant_id=tenant_id,
        employee_id__startswith=base_id
    ).values_list('employee_id', flat=True)

    if base_id not in existing_ids:
        return base_id

    # Handle collisions with postfix
    for suffix in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        candidate_id = f"{base_id}-{suffix}"
        if candidate_id not in existing_ids:
            return candidate_id

    # If all alphabetic suffixes are taken, use UUID
    return f"{base_id}-{str(uuid.uuid4())[:4].upper()}"

def is_nan_value(value):
    """
    Check if value is NaN (works without pandas/numpy)
    """
    if value is None:
        return True
    if isinstance(value, str) and value.strip().lower() in ['nan', 'null', '']:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    return False

def clean_decimal_value(value):
    """
    Clean and convert value to decimal - lightweight version without pandas
    """
    try:
        # Handle None and NaN values first
        if is_nan_value(value):
            return Decimal('0.00')
        
        # Convert to string and clean
        str_value = str(value).strip()
        
        # Remove common non-numeric characters
        cleaned = str_value.replace(',', '').replace('%', '').replace('$', '')
        
        # Handle empty string
        if not cleaned:
            return Decimal('0.00')
        
        # Convert to decimal
        return Decimal(cleaned).quantize(Decimal('0.01'))
    
    except (InvalidOperation, ValueError, TypeError):
        return Decimal('0.00')

def clean_int_value(value):
    """
    Clean and convert value to integer - lightweight version without pandas
    """
    try:
        # Handle None and NaN values first
        if is_nan_value(value):
            return 0
        
        # Convert to string and clean
        str_value = str(value).strip()
        
        # Remove common non-numeric characters
        cleaned = str_value.replace(',', '').replace('.0', '')
        
        # Handle empty string
        if not cleaned:
            return 0
        
        # Convert to int
        return int(float(cleaned))
    
    except (ValueError, TypeError):
        return 0

def clean_string_value(value):
    """
    Enhanced to handle NaN values without pandas
    """
    # Handle NaN first
    if is_nan_value(value):
        return ""
    
    # Convert to string and clean
    try:
        str_value = str(value).strip()
        return str_value if str_value.lower() not in ['nan', 'null', 'none'] else ""
    except (TypeError, AttributeError):
        return ""

def format_currency(amount):
    """Format amount as currency"""
    try:
        if is_nan_value(amount):
            return "₹0.00"
        
        # Convert to decimal
        decimal_amount = clean_decimal_value(amount)
        return f"₹{decimal_amount:,.2f}"
    except:
        return "₹0.00"

def calculate_percentage(part, total):
    """Calculate percentage without numpy"""
    try:
        if is_nan_value(part) or is_nan_value(total) or float(total) == 0:
            return 0.0
        
        percentage = (float(part) / float(total)) * 100
        return round(percentage, 2)
    except:
        return 0.0