import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler as rest_handler

c_fmt = "[%(levelname)s]%(asctime)s %(filename)s.%(funcName)s():line %(lineno)d :\n%(message)s"
date_format = "%Y-%m-%d %H:%M:%S %a"
logging.basicConfig(level=logging.INFO, format=c_fmt, datefmt=date_format)
logger = logging.getLogger("drf")


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
