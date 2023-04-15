"""
MIDDLEWARE
"""


class SaveClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def save_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.ip = self.save_client_ip(request)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
