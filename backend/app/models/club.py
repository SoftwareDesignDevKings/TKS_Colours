import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    colour: Mapped[str] = mapped_column(String(7), default="#6366f1", nullable=False)
    # Self-join: if this club is a sub-club (e.g. Cyber / AI under Programming)
    parent_club_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("clubs.id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    parent: Mapped[Optional["Club"]] = relationship(
        "Club", remote_side="Club.id", back_populates="sub_clubs"
    )
    sub_clubs: Mapped[list["Club"]] = relationship(
        "Club", back_populates="parent"
    )
    criteria: Mapped[list["Criterion"]] = relationship(
        back_populates="club", cascade="all, delete-orphan"
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="club"
    )
