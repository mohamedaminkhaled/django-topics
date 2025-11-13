from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class MiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_hello_includes_request_id_and_timing(self):
        resp = self.client.get("/api/hello/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # request_id set by RequestIDMiddleware
        self.assertIn("request_id", data)
        self.assertIsNotNone(data["request_id"])
        # timing set by RequestTimingMiddleware
        self.assertIn("timing", data)
        # headers added
        self.assertIn("X-Request-ID", resp)
        self.assertIn("X-Timing-ms", resp)

    def test_short_circuit_middleware(self):
        resp = self.client.get("/api/hello/", HTTP_X_SHORT="1")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("short"), True)

    def test_exception_middleware(self):
        resp = self.client.get("/api/error/")
        self.assertEqual(resp.status_code, 500)
        data = resp.json()
        self.assertIn("error", data)

    def test_per_view_middleware_decorator(self):
        # Create a small view that we will decorate in tests by importing wrapper
        from .views import hello_view
        from .middleware import per_view_middleware
        # wrap function and call via client by registering a temporary URL isn't trivial in test,
        # but we can at least assert decorator returns HttpResponse header when applied directly:
        wrapped = per_view_middleware(hello_view)
        response = wrapped(self.client.request().wsgi_request)
        self.assertEqual(response["X-Per-View"], "1")
