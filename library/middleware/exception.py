import json
import logging
import traceback

from django.http import JsonResponse

logger = logging.getLogger('weg.log')


class ExceptionBoxMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        try:
            ret_json = {
                'detail': '{}: {}'.format(exception.__class__.__name__, getattr(exception, 'message', ''))
            }
            response = JsonResponse(ret_json)
            response.status_code = getattr(exception, 'status_code', 500)
            _logger = logger.error if response.status_code >= 500 else logger.warning
            _logger(
                'status_code->{status_code}, error_code->{code}, url->{url}, '
                'method->{method}, param->{param}, '
                'traceback->{traceback}'.format(
                    status_code=response.status_code, code=exception.__class__.__name__, url=request.path,
                    method=request.method, param=json.dumps(getattr(request, request.method, {})),
                    traceback=traceback.format_exc()
                ))
            return response
        except Exception as e:
            response = JsonResponse(
                data={
                    'detail': getattr(e, 'message', ''),
                }
            )
            response.status_code = getattr(e, 'status_code', 500)
            logger.error(e, exc_info=True)
            return response
