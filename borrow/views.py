from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from datetime import timedelta, datetime
from .models import BorrowTransaction
from .serializers import BorrowTransactionSerializer
from books.models import Book


class BorrowTransactionViewSet(viewsets.ModelViewSet):
    queryset = BorrowTransaction.objects.all()
    serializer_class = BorrowTransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Handles book borrowing"""
        user = request.user
        book_id = request.data.get('book')
        return_date = request.data.get('return_date')

        # Convert return_date to date object
        try:
            return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid return date format. Use YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user has already borrowed this book and hasn't returned it
        if BorrowTransaction.has_active_borrow(user, book_id):
            return Response({"error": "You have already borrowed this book and must return it before borrowing again."},
                            status=status.HTTP_400_BAD_REQUEST)
        # Check borrowing limit
        if not BorrowTransaction(user=user).can_borrow_more_books():
            return Response({"error": "You must return a book before borrowing another."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Fetch book
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        # Validate return date
        max_return_date = now().date() + timedelta(days=30)
        if return_date > max_return_date:
            return Response({"error": "Return date cannot exceed 30 days."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Borrow book
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()
            borrow = BorrowTransaction.objects.create(
                user=user, book=book, return_date=return_date)
            return Response(BorrowTransactionSerializer(borrow).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Book is not available."}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Handle book return"""
        borrow = self.get_object()
        if borrow.returned:
            return Response({"error": "Book already returned."}, status=status.HTTP_400_BAD_REQUEST)

        borrow.returned = True
        borrow.save()
        borrow.book.available_copies += 1
        borrow.book.save()

        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)
