# Tenant Resolution Utility - Domain-Free Multi-Tenant
# Each user gets their own workspace, no domain complexity

import logging

logger = logging.getLogger(__name__)

def resolve_tenant_for_request(request):
    """
    Domain-free tenant resolution for authenticated users.
    
    Each user should have their own tenant (workspace) assigned during signup.
    No auto-assignment to prevent data leakage between companies.
    
    Returns:
        Tenant object or None
    """
    # Check if tenant already resolved
    tenant = getattr(request, 'tenant', None)
    if tenant and tenant.is_active:
        return tenant
    
    # Try to resolve from authenticated user
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            # Get tenant from user (should have been assigned during signup)
            user_tenant = getattr(request.user, 'tenant', None)
            if user_tenant and user_tenant.is_active:
                # Set tenant in request for downstream processing
                request.tenant = user_tenant
                logger.info(f"Resolved tenant from authenticated user: {user_tenant.name}")
                return user_tenant
            else:
                # User has no tenant - this is a signup/configuration issue
                logger.error(f"User {request.user.email} has no tenant assigned. Each user should have their own workspace.")
                # DO NOT auto-assign to existing tenants for security
                # This prevents data leakage between different companies
                
        except Exception as e:
            logger.error(f"Error resolving tenant for user {request.user.email}: {e}")
    
    return None

def get_tenant_or_error(request):
    """
    Get tenant for request or return error response.
    
    Returns:
        tuple: (tenant, error_response)
        - If successful: (tenant_object, None)
        - If failed: (None, Response_object)
    """
    from rest_framework.response import Response
    
    tenant = resolve_tenant_for_request(request)
    
    if not tenant:
        error_response = Response({
            "error": "No tenant found. Please ensure you're signed up and have a valid workspace.",
            "details": "No active tenants found in the system. Please contact administrator."
        }, status=400)
        return None, error_response
    
    return tenant, None