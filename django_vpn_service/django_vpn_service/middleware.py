from django.middleware.common import CommonMiddleware
from django.shortcuts import redirect
from django.urls import resolve


class Redirect404Middleware(CommonMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        requested_url = request.path
        allow_404 = False

        try:
            match = resolve(requested_url)
            url_name = match.url_name
            # if it is endpoints for proxying, ignore 404 error and do not redirect
            if url_name in ("proxy_data", "proxy_site"):
                allow_404 = True
        except Exception as e:
            pass

        response = self.get_response(request)
        if self.should_redirect_with_slash(request):
            return response
        if response.status_code == 404 and not allow_404:
            return redirect("home")
        return response
