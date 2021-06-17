import logging

from django.db import DatabaseError
from rest_framework import status
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
    if response is None:
        logger.error('%s,%s' % (context_view, exc))
        if isinstance(exc, DatabaseError):
            detail = 'Database operation error, please check data or your operation to data'
        else:
            detail = str(exc).replace('\\', '')
        response = Response(
            data={'detail': detail},
            status=status.HTTP_400_BAD_REQUEST
        )
    return response
