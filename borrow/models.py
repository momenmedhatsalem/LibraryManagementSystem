from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book
from datetime import timedelta, date

User = get_user_model()


class BorrowTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField()
    returned = models.BooleanField(default=False)
    penalty = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def calculate_penalty(self):
        """Calculate penalty if book is overdue"""
        if self.returned:
            return 0
        today = date.today()
        if today > self.return_date:
            days_late = (today - self.return_date).days
            return days_late * 5  # Example: $5 per late day
        return 0

    def can_borrow_more_books(self):
        """Check if user can borrow more books"""
        return BorrowTransaction.objects.filter(user=self.user, returned=False).count() < 3

    @staticmethod
    def has_active_borrow(user, book):
        """Check if user has already borrowed the book and not returned it"""
        return BorrowTransaction.objects.filter(user=user, book=book, returned=False).exists()
    
    def save(self, *args, **kwargs):
        self.penalty = self.calculate_penalty()
        super().save(*args, **kwargs)
