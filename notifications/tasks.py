from celery import shared_task
from django.utils import timezone
from dotenv import load_dotenv

from borrowings.models import Borrowing
from notifications.bot import send_telegram_message

load_dotenv()


@shared_task(ignore_result=True)
def send_overdue_borrowing_notifications() -> None:
    """Sends a notification to the managers about the overdue borrowings."""
    message = "No borrowings overdue today!"
    overdue_borrowings = Borrowing.objects.filter(
        expected_return__lt=timezone.now() - timezone.timedelta(days=1),
        actual_return__isnull=True,
    )

    if overdue_borrowings.exists():
        message = "The following borrowings are overdue:\n"

        for borrowing in overdue_borrowings:
            book_title = borrowing.book.title
            user_email = borrowing.user.email
            message += f"id: {borrowing.id} ({book_title} - {user_email})\n"

    send_telegram_message(message=message)
