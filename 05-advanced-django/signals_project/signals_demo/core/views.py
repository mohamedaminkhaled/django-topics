from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from .custom_signals import user_action_signal

def trigger_custom_signal(request):
    user_action_signal.send(
        sender=None,
        user="mohamed",
        action="clicked_button"
    )
    return JsonResponse({"message": "Custom signal sent!"})


def trigger_error(request):
    1 / 0  # will trigger got_request_exception signal
    return JsonResponse({"ok": True})
