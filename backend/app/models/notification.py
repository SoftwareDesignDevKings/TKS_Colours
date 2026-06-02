import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.database import Base


class NotificationType(str, enum.Enum):
    CRITERIA_MET = "criteria_met"
    REMINDER_DUE = "reminder_due"
    APPLICATION_APPROVED = "application_approved"
    APPLICATION_REJECTED = "application_rejected"


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Polymorphic link — either student or application context
    student_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("students.id", ondelete="CASCADE"), nullable=True
    )
    application_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("applications.id", ondelete="CASCADE"), nullable=True
    )
    club_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("clubs.id"), nullable=True
    )
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    student: Mapped[Optional["Student"]] = relationship()
    application: Mapped[Optional["Application"]] = relationship()
    club: Mapped[Optional["Club"]] = relationship()
