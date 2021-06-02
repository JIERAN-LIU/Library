from django.urls import include, path
from rest_framework import routers

from book import views
#setting
router = routers.DefaultRouter()
router.register('book', views.BookViewSet)
router.register('author', views.AuthorViewSet)
router.register('copy', views.BookCopyViewSet)
router.register('publisher', views.PublisherViewSet)

app_name = 'book'

urlpatterns = [
    path('', include(router.urls)),
]
