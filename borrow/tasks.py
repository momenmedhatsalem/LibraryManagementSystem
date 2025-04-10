from .models import BorrowTransaction
from django.utils.timezone import now
from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_email_task(to_email, subject, message):
    """Send an email asynchronously using Celery."""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email="library@example.com",
            recipient_list=[to_email],
            fail_silently=False,
        )
        logger.info(
            f"Email sent successfully to {to_email} with subject: {subject}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")


@shared_task
def send_due_date_reminders():
    """Send reminder emails to users with books due in 3 days or less."""
    today = now().date()
    due_transactions = BorrowTransaction.objects.filter(
        returned=False,
        return_date__range=(today, today + timedelta(days=3))
    ).select_related("user", "book")  # Optimize query

    email_tasks = []
    for transaction in due_transactions:
        subject = "Return Reminder: Book Due Soon"
        message = f"Dear {transaction.user.username},\n\nYour book '{transaction.book.title}' is due on {transaction.return_date}. Please return it on time."
        email_tasks.append(send_email_task.s(
            transaction.user.email, subject, message))

    if email_tasks:
        from celery import group
        group(*email_tasks).apply_async()  # Send emails in parallel
