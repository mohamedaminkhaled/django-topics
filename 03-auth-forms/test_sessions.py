
"""
To test this code please follow SESSIONS_SHELL.md
"""
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse

# Create fake request
rf = RequestFactory()
request = rf.get('/')

# Apply SessionMiddleware manually (like Django does)
middleware = SessionMiddleware(lambda req: HttpResponse("OK"))
middleware.process_request(request)

# Check what's created
print("New session object:", request.session)
print("Session key before save:", request.session.session_key)

# Set some data
request.session['theme'] = 'dark'
request.session['recent_items'] = [1, 2, 3]
request.session.save()  # Django normally does this at response time

print("Session key after save:", request.session.session_key)

# Simulate the response
response = HttpResponse("Done")
middleware.process_response(request, response)

# Cookie now attached
print("Cookie set:", response.cookies['sessionid'].value)
