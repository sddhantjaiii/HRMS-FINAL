# Tenant Resolution Utility
# This utility provides a consistent way to resolve tenant for authenticated users

import logging

logger = logging.getLogger(__name__)

def resolve_tenant_for_request(request):
    """
    Smart tenant resolution for authenticated users.
    
    Priority:
    1. Check if tenant already set in request
    2. Get tenant from authenticated user 
    3. Try to find any active tenant (for single company setups)
    4. Optionally assign default tenant to user
    
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
            # Get tenant from user
            user_tenant = getattr(request.user, 'tenant', None)
            if user_tenant and user_tenant.is_active:
                # Set tenant in request for downstream processing
                request.tenant = user_tenant
                logger.info(f"Resolved tenant from authenticated user: {user_tenant.name}")
                return user_tenant
            else:
                # Try to find or create a default tenant for this user
                logger.warning(f"User {request.user.email} has no active tenant, attempting to resolve...")
                
                # Import here to avoid circular imports
                from ..models import Tenant
                
                # Try to get any active tenant (for single company setups)
                default_tenant = Tenant.objects.filter(is_active=True).first()
                if default_tenant:
                    logger.info(f"Using default tenant for user: {default_tenant.name}")
                    # Optionally assign this tenant to the user if they don't have one
                    if not request.user.tenant:
                        request.user.tenant = default_tenant
                        request.user.save()
                        logger.info(f"Assigned default tenant to user {request.user.email}")
                    # Set tenant in request
                    request.tenant = default_tenant
                    return default_tenant
                else:
                    logger.error("No active tenants found in the system")
                    
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