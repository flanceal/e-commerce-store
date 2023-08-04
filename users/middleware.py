from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlparse
from django.conf import settings


class PreviousPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_urls = [reverse('users:login'), reverse('users:logout'), reverse('users:password-change'), reverse('users:registration'), '/product_images/']
        if not any(request.path_info.startswith(url) for url in excluded_urls):
            if not request.user.is_authenticated:
                previous_page = settings.DOMAIN_NAME + request.path_info
                parsed_url = urlparse(previous_page)
                if parsed_url.netloc == request.get_host():
                    request.session['previous_page'] = previous_page
        response = self.get_response(request)
        return response
