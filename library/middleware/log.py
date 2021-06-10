import json
import logging

from django.utils.deprecation import MiddlewareMixin


class RequestLogMiddleware(MiddlewareMixin):
    """
    Global logger middleware, bound request's information to request thread
    then filter get log information from local thread
    """

    def __init__(self, get_response=None):
        super(RequestLogMiddleware, self).__init__(get_response)
        self.apiLogger = logging.getLogger('web.log')

    def __call__(self, request):
        try:
            if request.body:
                body = json.loads(request.body)
            else:
                body = dict()
        except Exception as e:
            self.apiLogger.error(e, exc_info=True)
            body = dict()

        if request.method == 'GET':
            body.update(dict(request.GET))
        else:
            body.update(dict(request.POST))
        log_info = {
            'body': body,
            'path': request.path,
            'method': request.method,
            'username': request.user.username,
            'sip': request.META.get('REMOTE_ADDR', ''),
        }

        response = self.get_response(request)

        if hasattr(response, 'data'):
            result = response.data
        elif hasattr(response, 'content'):
            result = str(response.content, encoding="utf-8")
        else:
            result = ''
        log_info.update({
            'status_code': response.status_code,
            'result': result,
        })
        self.apiLogger.info(log_info)

        return response
