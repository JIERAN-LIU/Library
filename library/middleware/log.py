import json
import logging
import threading

from django.utils.deprecation import MiddlewareMixin

local = threading.local()


class RequestLogFilter(logging.Filter):
    """
    Logger filter
    """

    def filter(self, record):
        for attr, value in local.__dict__.items():
            if attr.startswith('__'):
                continue
            record.__setattr__(attr, value)

        return True


class RequestLogMiddleware(MiddlewareMixin):
    """
    Global logger middleware, bound request's information to request thread
    then filter get log information from local thread
    """

    def __init__(self, get_response=None):
        super(RequestLogMiddleware, self).__init__(get_response)

        self.apiLogger = logging.getLogger('web.log')
        self.console_logger = logging.getLogger('default')

    def __call__(self, request):
        try:
            body = json.loads(request.body)
        except Exception as e:
            body = dict()

        if request.method == 'GET':
            body.update(dict(request.GET))
        else:
            body.update(dict(request.POST))

        local.body = body
        local.path = request.path
        local.method = request.method
        local.username = request.user
        local.sip = request.META.get('REMOTE_ADDR', '')
        local.dip = 'none'

        response = self.get_response(request)
        local.status_code = response.status_code
        local.reason_phrase = response.reason_phrase
        if hasattr(response, 'data'):
            local.result = response.data
        elif hasattr(response, 'content'):
            local.result = str(response.content, encoding="utf-8")
        else:
            local.result = 'none'

        self.apiLogger.info(msg='system auto log')

        self._log_in_console()

        return response

    def _log_in_console(self):
        log_info = {}
        for attr, value in local.__dict__.items():
            log_info[attr] = value or 'none'
        self.console_logger.info(log_info)
