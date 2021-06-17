from django.urls import include, path
from rest_framework import routers

from search import views

router = routers.DefaultRouter()
router.register('book', views.BookSearchViewSet, basename='book-search')
router.register('author', views.AuthorSearchViewSet, basename='author-search')
router.register('publisher', views.PublisherSearchViewSet, basename='publisher-search')
router.register('complete/book', views.BookAutocompleteSearchViewSet, basename='auto-complete')

app_name = 'search'

urlpatterns = [
    path('search/', include(router.urls)),
]
