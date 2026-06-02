import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    application_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # The staff member to remind
    staff_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("staff.id"), nullable=True
    )
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    application: Mapped["Application"] = relationship(back_populates="reminders")
    staff: Mapped[Optional["Staff"]] = relationship()
