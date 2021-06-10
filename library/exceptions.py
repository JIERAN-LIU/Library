import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler as rest_handler

logger = logging.getLogger("web.log")


def library_global_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    """
    :param exc: exception
    :param context: request context
    :return: Response object
    """

    response = rest_handler(exc, context)
    context_view = context.get("view", None)
    context_path = context.get('request').path
    context_method = context.get('request').method
    context_ip = context.get('request').META.get("REMOTE_ADDR")
    if response is None:
        logger.error('%s,%s' % (context_view, exc))
        response = Response(
            {'success': False, 'msg': str(exc).replace('\\', ''), "path": context_path, "method": context_method,
             'remote_address': context_ip})
    return response
