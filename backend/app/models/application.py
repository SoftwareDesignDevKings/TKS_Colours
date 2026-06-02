import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.database import Base


class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    club_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("clubs.id"), nullable=False, index=True
    )
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status"),
        default=ApplicationStatus.PENDING,
        nullable=False,
        index=True,
    )
    # Set automatically when criteria engine fires
    auto_triggered: Mapped[bool] = mapped_column(default=True, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    applied_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    decided_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    decided_by_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("staff.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    student: Mapped["Student"] = relationship(back_populates="applications")
    club: Mapped["Club"] = relationship(back_populates="applications")
    decided_by: Mapped[Optional["Staff"]] = relationship()
    reminders: Mapped[list["Reminder"]] = relationship(
        back_populates="application", cascade="all, delete-orphan"
    )
