from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowTransactionViewSet

router = DefaultRouter()
router.register(r'', BorrowTransactionViewSet,
                basename='borrow')  # No "borrow" prefix

urlpatterns = [
    path('', include(router.urls)),
]
