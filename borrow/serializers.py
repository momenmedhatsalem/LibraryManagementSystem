from rest_framework import serializers
from django.utils.timezone import now
from datetime import timedelta
from .models import BorrowTransaction
from users.models import User
from books.models import Book


class BorrowTransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show username
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all())  # Accept book ID

    class Meta:
        model = BorrowTransaction
        fields = '__all__'

    def validate_return_date(self, value):
        """Ensure return date is within 30 days"""
        max_return_date = now().date() + timedelta(days=30)
        if value > max_return_date:
            raise serializers.ValidationError(
                "Return date cannot exceed 30 days.")
        return value
