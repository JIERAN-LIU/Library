from django.urls import include, path
from rest_framework import routers

from recommendation import views

router = routers.DefaultRouter()
router.register('book-recommend', views.BookRecommendation, basename='recommendation')

app_name = 'recommendation'

urlpatterns = [
    path('', include(router.urls)),
]
