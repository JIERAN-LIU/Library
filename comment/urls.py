from django.urls import include, path
from rest_framework import routers

from comment import views

router = routers.DefaultRouter()
router.register('comment', views.CommentViewSet)

app_name = 'comment'

urlpatterns = [
    path('', include(router.urls)),
]
