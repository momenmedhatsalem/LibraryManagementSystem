from rest_framework import viewsets, filters
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework.exceptions import ValidationError
from .models import Library
from .serializers import LibrarySerializer


class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = Library.objects.all()

        # 🔹 Filter by book category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(
                books__category_id=category_id).distinct()

        # 🔹 Filter by author
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(books__author_id=author_id).distinct()

        # 🔹 Calculate distance based on user's location
        user = self.request.user
        if user.is_authenticated and user.location:
            if isinstance(user.location, Point):  # Ensure the location is a valid Point
                user_location = user.location
                queryset = queryset.annotate(
                    distance=Distance('location', user_location)
                ).order_by('distance')  # Sort by distance (ascending)
            else:
                raise ValidationError("User location is not a valid Point.")
        else:
            raise ValidationError(
                "User location is required to calculate distances.")

        return queryset
