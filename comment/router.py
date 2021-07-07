from rest_framework.routers import DefaultRouter


class StandardRouter(DefaultRouter):
    def __init__(self, trailing_slash='/?'):
        super(StandardRouter, self).__init__()
        self.trailing_slash = trailing_slash
