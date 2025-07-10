import time
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy

class IdleTimeoutMiddleware:
    """
    Logs out any user who’s been idle for more than the idle_limit (in seconds).
    Does NOT touch the cookie expiry (that’s handled by SESSION_COOKIE_AGE).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = int(time.time())  # Current time in seconds
            last_activity = request.session.get('last_activity', now)  # Default to current time if not found

            # Set the idle timeout (e.g., 5 minutes, 300 seconds)
            idle_limit = 300  # 5 minutes in seconds (can be adjusted as needed)

            if (now - last_activity) > idle_limit:
                # Too long since the last request → force logout
                logout(request)
                return redirect(reverse_lazy('Login'))  # Redirect to the login page

            # Otherwise, update last_activity to the current time
            request.session['last_activity'] = now

        return self.get_response(request)
