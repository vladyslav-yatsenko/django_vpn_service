from django.shortcuts import redirect
from django.middleware.common import CommonMiddleware


class Redirect404Middleware(CommonMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if self.should_redirect_with_slash(request):
            return response
        if response.status_code == 404:
            return redirect("home")
        return response