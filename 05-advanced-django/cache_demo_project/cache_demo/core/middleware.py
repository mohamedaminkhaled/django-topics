import logging
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Simple middleware to log request path and cache-hit info.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        logger.info(f"Response status: {getattr(response, 'status_code', 'unknown')}")
        return response
