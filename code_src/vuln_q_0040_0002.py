from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import debug_exceptions
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def cors_allow_all(origin: Optional[str] = None) -> HttpResponseForbidden:
    """
    Configures CORS to allow all origins with proper logging and security checks.
    
    Args:
        origin: Optional origin to validate against whitelist
        
    Returns:
        HttpResponseForbidden if origin is invalid or not allowed
    """
    # Validate input
    if origin is not None and not isinstance(origin, str):
        logger.error(f"Invalid origin type: {type(origin)}")
        return HttpResponseForbidden("Invalid origin")

    # Default to allowing all origins
    allowed_origins = ["*"]
    
    # Validate origin if provided
    if origin:
        # Remove any whitespace and validate format
        origin = origin.strip()
        if not origin.startswith("http://") and not origin.startswith("https://"):
            logger.warning(f"Invalid origin format: {origin}")
            return HttpResponseForbidden("Invalid origin format")
        
        # Check against whitelist
        if origin not in allowed_origins:
            logger.warning(f"Origin {origin} not in whitelist")
            return HttpResponseForbidden("Origin not allowed")

    # Log the request
    logger.info(f"CORS request from origin: {origin}")

    # Return CORS headers
    response = HttpResponseForbidden()
    response["Access-Control-Allow-Origin"] = origin if origin else "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
    
    return response

@csrf_exempt
@debug_exceptions
def cors_handler(request):
    """
    Handler for CORS preflight requests.
    
    Args:
        request: Incoming HTTP request
        
    Returns:
        HttpResponse with CORS headers
    """
    return cors_allow_all()