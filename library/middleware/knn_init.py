import logging

from django.core.exceptions import MiddlewareNotUsed

from recommendation.models import Recommendation


class InitKNNModel(object):
    def __init__(self, get_response):
        self.get_response = get_response
        logger = logging.getLogger('default')

        logger.info('=====Initial KNN model by book comment=====')
        Recommendation()
        logger.info('=====KNN model training done=====')

        raise MiddlewareNotUsed

    def __call__(self, request):
        response = self.get_response(request)
        return response
