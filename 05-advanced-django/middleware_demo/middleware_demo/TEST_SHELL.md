from django.test import RequestFactory
from django.http import HttpResponse
from asgiref.sync import sync_to_async
from core.middleware import (
    RequestIDMiddleware, TimingMiddleware,
    ViewLoggingMiddleware, ExceptionHandlingMiddleware
)

# Create a fake request
factory = RequestFactory()
request = factory.get("/api/hello/")

# Dummy view to simulate Django view
def dummy_view(request):
    return HttpResponse("Hello Middleware!")

# ------------------------------
# Test 1️⃣ - RequestIDMiddleware 
# ------------------------------
mw1 = RequestIDMiddleware(lambda req: dummy_view(req))
response = asyncio.run(mw1(request))
print("Response headers:", response.headers)

# ---- if the code is not async and you want to run it async

factory = RequestFactory()
request = factory.get("/api/hello/")

def dummy_view(request):
    return HttpResponse("Hello Middleware!")

# Wrap sync view so it can be awaited
async_dummy_view = sync_to_async(dummy_view)

mw1 = RequestIDMiddleware(async_dummy_view)

response = asyncio.run(mw1(request))

print("Response:", response)
print("Headers:", response.headers)

# ------------------------------
# Test 2️⃣ - TimingMiddleware
# ------------------------------
mw2 = TimingMiddleware(lambda req: dummy_view(req))
response = asyncio.run(mw2(request))
print("Elapsed time header:", response.headers.get("X-Elapsed-Time"))

# ------------------------------
# Test 3️⃣ - ViewLoggingMiddleware (old-style)
# ------------------------------
mw3 = ViewLoggingMiddleware(lambda req: dummy_view(req))
mw3.process_view(request, dummy_view, (), {})
response = dummy_view(request)
response = mw3.process_response(request, response)
print("ViewLoggingMiddleware done ✅")

# ------------------------------
# Test 4️⃣ - ExceptionHandlingMiddleware
# ------------------------------
def bad_view(request):
    raise ValueError("Something broke!")

mw4 = ExceptionHandlingMiddleware(lambda req: bad_view(req))
try:
    response = mw4.process_request(request)
    if response is None:
        response = bad_view(request)
except Exception as e:
    response = mw4.process_exception(request, e)

print("ExceptionHandlingMiddleware response:", response.content)
