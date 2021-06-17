from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.views.static import serve
from rest_framework import routers

from common import views
from common.views import ImageUploadViewSet

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('college', views.CollegeViewSet)

app_name = 'common'

urlpatterns = [
    path('', include(router.urls)),
    url(r'^user/login', views.UserLoginViewSet.as_view()),
    url(r'^user/logout', views.UserLogoutViewSet.as_view()),
    url(r'^user/pwd', views.PasswordUpdateViewSet.as_view()),
    url(r'^dict', views.ConstantViewSet.as_view()),
    url(r'upload/$', ImageUploadViewSet.as_view()),
    url(r'upload/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})
]
