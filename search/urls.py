from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

app_name = 'search'

urlpatterns = [
    path('search/', include(router.urls)),
]
