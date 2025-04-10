from django.db.models import Count
from .serializers import AuthorSerializer
from .models import Author
from django.db.models import Count, Q
from .serializers import BookSerializer
from .models import Book
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from .models import Book, Author, Category
from .serializers import BookSerializer, AuthorSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = Author.objects.annotate(book_count=Count(
            'books', distinct=True)) 

        library_id = self.request.query_params.get('library')
        category_id = self.request.query_params.get('category')

        if library_id:
            queryset = queryset.filter(books__library_id=library_id).distinct()

        if category_id:
            queryset = queryset.filter(
                books__category_id=category_id).distinct()

        return queryset

from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404
from .models import Author
from .serializers import LoadedAuthorSerializer


class LoadedAuthorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoadedAuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = Author.objects.prefetch_related('books__category').all()

        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(
                books__category_id=category_id).distinct()

        return queryset



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # Filtering by category, library, and author
    filterset_fields = ['category', 'library', 'author']

    # Searching by book title, author name, and category name
    search_fields = ['title', 'author__name', 'category__name']
