from rest_framework import serializers
from .models import Library


from rest_framework import serializers


class LibrarySerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Library
        fields = ['id', 'name', 'location', 'distance', 'created_at']

    def get_distance(self, obj):
        # Ensure distance is a float value
        distance = getattr(obj, 'distance', None)
        if distance:
            return distance.m
        return None
