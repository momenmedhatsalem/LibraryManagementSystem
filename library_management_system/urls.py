from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from library.views import LibraryViewSet
from books.views import BookViewSet, AuthorViewSet, LoadedAuthorViewSet, CategoryViewSet
from borrow.views import BorrowTransactionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'libraries', LibraryViewSet)
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'loaded-authors', LoadedAuthorViewSet,
                basename='loaded-author')
router.register(r'categories', CategoryViewSet)
router.register(r'borrow', BorrowTransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),  # Include Auth Endpoints
    path('api/borrow', include('borrow.urls')),  # Borrowing system
    path('api/', include(router.urls)),
]