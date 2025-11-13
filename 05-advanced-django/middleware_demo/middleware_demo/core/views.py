from django.http import JsonResponse
from django.template.response import TemplateResponse

import asyncio
import os
from django.http import FileResponse, Http404
from django.conf import settings

def well_known_file(request, path):
    """
    Serve files from the .well-known directory safely.
    Example: GET /.well-known/assetlinks.json
    """
    well_known_root = os.path.join(settings.BASE_DIR, ".well-known")
    file_path = os.path.join(well_known_root, path)

    if not os.path.exists(file_path):
        raise Http404("File not found")

    return FileResponse(open(file_path, "rb"))

async def hello_view(request):
    await asyncio.sleep(0.1)
    return JsonResponse({"message": "Hello, async world!"})

def error_view(request):
    """Raises an exception to test ExceptionHandlingMiddleware."""
    raise ValueError("Intentional error from view")

def template_view(request):
    """Returns a TemplateResponse for TemplateResponseMiddleware demo."""
    context = {"user": "Mohamed", "message": "Hello from TemplateResponse!"}
    return TemplateResponse(request, "hello.html", context)
