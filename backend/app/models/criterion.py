import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Criterion(Base):
    __tablename__ = "criteria"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    club_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("clubs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    # How many times/evidence items must be logged to satisfy this criterion
    required_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    # If the criterion only applies to specific year groups (NULL = all years)
    year_group_applicable: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    # Display order within the club
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    club: Mapped["Club"] = relationship(back_populates="criteria")
    achievements: Mapped[list["Achievement"]] = relationship(
        back_populates="criterion", cascade="all, delete-orphan"
    )
