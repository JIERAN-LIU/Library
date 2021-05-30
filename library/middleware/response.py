from django.utils.deprecation import MiddlewareMixin


class RemoveRealm(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 401:
            del response['WWW-Authenticate']
        return response
