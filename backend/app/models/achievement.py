import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    criterion_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("criteria.id", ondelete="CASCADE"), nullable=False, index=True
    )
    logged_by_staff_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("staff.id"), nullable=True
    )
    # Free-text evidence note from staff
    evidence_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Optional URL to external evidence (e.g. Google Drive, portfolio link)
    evidence_url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    achieved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    student: Mapped["Student"] = relationship(back_populates="achievements")
    criterion: Mapped["Criterion"] = relationship(back_populates="achievements")
    logged_by: Mapped[Optional["Staff"]] = relationship()
