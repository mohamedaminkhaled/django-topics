import uuid
import time
import asyncio
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

logger = logging.getLogger(__name__)


# -------------------------------
# 1️⃣ RequestIDMiddleware (async + sync safe)
# -------------------------------
class RequestIDMiddleware:
    """Adds a request_id and X-Request-ID header (async + sync compatible)."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.is_async = asyncio.iscoroutinefunction(get_response)

    def __call__(self, request):
        logger.info(">>> Enter RequestIDMiddleware (request)")
        rid = str(uuid.uuid4())
        request.request_id = rid
        # logger.debug(f"[RequestIDMiddleware] assigned id={rid}")

        if self.is_async:
            return self._async_call(request)
        else:
            response = self.get_response(request)
            response["X-Request-ID"] = rid
            logger.info("<<< Exit RequestIDMiddleware (response)")
            return response

    async def _async_call(self, request):
        response = await self.get_response(request)
        response["X-Request-ID"] = request.request_id
        logger.info("<<< Exit RequestIDMiddleware (async response)")
        return response


# -------------------------------
# 2️⃣ TimingMiddleware (async + sync safe)
# -------------------------------
class TimingMiddleware:
    """Measure total time taken by the view (async + sync safe)."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.is_async = asyncio.iscoroutinefunction(get_response)

    def __call__(self, request):
        logger.info(">>> Enter TimingMiddleware (request)")
        start = time.perf_counter()

        if self.is_async:
            return self._async_call(request, start)
        else:
            response = self.get_response(request)
            elapsed = time.perf_counter() - start
            response["X-Elapsed-Time"] = f"{elapsed:.4f}"
            # logger.info(f"[TimingMiddleware] Took {elapsed:.4f}s")
            logger.info("<<< Exit TimingMiddleware (response)")
            return response

    async def _async_call(self, request, start):
        response = await self.get_response(request)
        elapsed = time.perf_counter() - start
        response["X-Elapsed-Time"] = f"{elapsed:.4f}"
        # logger.info(f"[TimingMiddleware] Took {elapsed:.4f}s")
        logger.info("<<< Exit TimingMiddleware (async response)")
        return response


# -------------------------------
# 3️⃣ ExceptionHandlingMiddleware
# -------------------------------
class ExceptionHandlingMiddleware(MiddlewareMixin):
    """Catch exceptions and return JSON response."""

    def process_exception(self, request, exception):
        logger.error(f"[ExceptionHandlingMiddleware] Exception: {exception}")
        return JsonResponse({"error": str(exception)}, status=500)


# -------------------------------
# 4️⃣ ViewLoggingMiddleware
# -------------------------------
class ViewLoggingMiddleware(MiddlewareMixin):
    """Logs view execution and adds request_id."""

    def process_request(self, request):
        logger.info(">>> Enter ViewLoggingMiddleware.process_request")
        request.request_id = str(uuid.uuid4())
        # logger.info(f"[ViewLoggingMiddleware] Assigned request_id={request.request_id}")

    def process_view(self, request, view_func, view_args, view_kwargs):
        logger.info(f"[ViewLoggingMiddleware] About to call view: {view_func.__name__}")

    def process_response(self, request, response):
        rid = getattr(request, "request_id", None)
        if rid:
            response["X-Request-ID"] = rid
        logger.info("<<< Exit ViewLoggingMiddleware.process_response")
        return response


# -------------------------------
# 5️⃣ TemplateResponseMiddleware
# -------------------------------
class TemplateResponseMiddleware(MiddlewareMixin):
    """Modify TemplateResponse before render."""

    def process_template_response(self, request, response):
        logger.info(">>> Enter TemplateResponseMiddleware.process_template_response")
        if hasattr(response, "context_data"):
            response.context_data["added_by_middleware"] = (
                "✅ Middleware modified template context"
            )
            # logger.info(f"[TemplateResponseMiddleware] Added context_data={response.context_data['added_by_middleware']}")
        logger.info("<<< Exit TemplateResponseMiddleware.process_template_response")
        return response
