from django.urls import include, path
from rest_framework import routers

from borrow import views

router = routers.DefaultRouter()
router.register('borrow', views.BorrowRecordViewSet)
router.register('return', views.BookCopyReturnViewSet)
router.register('renew', views.BookCopyRenewViewSet)
router.register('fine', views.BookCopyFineViewSet)

app_name = 'borrow'

urlpatterns = [
    path('', include(router.urls)),
]
