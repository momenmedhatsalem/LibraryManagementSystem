from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta
from .models import BorrowTransaction
from .tasks import send_email_task


@receiver(post_save, sender=BorrowTransaction)
def send_borrow_confirmation_email(sender, instance, created, **kwargs):
    """Trigger Celery task to send an email when a book is borrowed."""
    if created:
        subject = "Borrowing Confirmation"
        message = f"Dear {instance.user.username},\n\nYou have borrowed '{instance.book.title}'. Please return it by {instance.return_date}."
        send_email_task.delay(instance.user.email, subject, message)


@receiver(post_save, sender=BorrowTransaction)
def send_return_confirmation_email(sender, instance, **kwargs):
    """Trigger Celery task to send an email when a book is returned."""
    if instance.returned:
        subject = "Book Returned Successfully"
        message = f"Dear {instance.user.username},\n\nThank you for returning '{instance.book.title}'."
        send_email_task.delay(instance.user.email, subject, message)
