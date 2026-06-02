"""
Reminder Service
----------------
Background scheduler that runs daily and sends email reminders for pending
applications that have gone unanswered past their due date.
"""
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.reminder import Reminder
from app.models.application import Application, ApplicationStatus
from app.models.student import Student
from app.models.club import Club
from app.models.staff import Staff
from app.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def process_due_reminders() -> int:
    """
    Find all unsent reminders that are past due and send email notifications.
    Returns the number of reminders processed.
    """
    async with AsyncSessionLocal() as db:
        now = datetime.utcnow()

        result = await db.execute(
            select(Reminder).where(
                Reminder.due_at <= now,
                Reminder.sent_at.is_(None),
                Reminder.acknowledged_at.is_(None),
            )
        )
        reminders = result.scalars().all()

        processed = 0
        for reminder in reminders:
            try:
                await _send_reminder_email(db, reminder)
                reminder.sent_at = now
                processed += 1
            except Exception as exc:
                logger.error(f"Failed to send reminder {reminder.id}: {exc}")

        await db.commit()
        logger.info(f"Processed {processed} reminders")
        return processed


async def _send_reminder_email(db: AsyncSession, reminder: Reminder) -> None:
    """Build and send a reminder email for a pending application."""
    from app.config import settings

    # Load related data
    app_result = await db.execute(
        select(Application).where(Application.id == reminder.application_id)
    )
    application = app_result.scalars().first()
    if not application or application.status != ApplicationStatus.PENDING:
        return

    student_result = await db.execute(
        select(Student).where(Student.id == application.student_id)
    )
    student = student_result.scalars().first()

    club_result = await db.execute(
        select(Club).where(Club.id == application.club_id)
    )
    club = club_result.scalars().first()

    subject = f"[TKS Colours] Reminder: Pending application for {student.name if student else 'a student'}"
    body = (
        f"This is a reminder that the following award application is still pending:\n\n"
        f"Student: {student.name if student else 'Unknown'}\n"
        f"Club: {club.name if club else 'Unknown'}\n"
        f"Applied: {application.applied_at.strftime('%d %b %Y')}\n\n"
        f"Please log into TKS Colours to review and make a decision.\n"
    )

    # If email is not configured, log to console only
    if not settings.MAIL_USERNAME:
        logger.info(f"[EMAIL STUB] To: staff | Subject: {subject}\n{body}")
        return

    # Real email sending — requires fastapi-mail to be configured
    try:
        from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )
        fm = FastMail(conf)
        # Send to all active staff if no specific staff assigned
        recipients = []
        if reminder.staff_id:
            staff_result = await db.execute(
                select(Staff).where(Staff.id == reminder.staff_id, Staff.is_active == True)
            )
            staff_member = staff_result.scalars().first()
            if staff_member:
                recipients = [staff_member.email]
        if not recipients:
            all_staff = await db.execute(select(Staff).where(Staff.is_active == True))
            recipients = [s.email for s in all_staff.scalars().all()]

        if recipients:
            message = MessageSchema(
                subject=subject,
                recipients=recipients,
                body=body,
                subtype=MessageType.plain,
            )
            await fm.send_message(message)
    except Exception as exc:
        logger.error(f"Email send failed: {exc}")
        raise
