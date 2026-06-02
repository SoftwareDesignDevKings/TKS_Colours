import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    year_group: Mapped[int] = mapped_column(nullable=False)
    # cohort_year: the calendar year the student started (e.g. 2023)
    cohort_year: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
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
    achievements: Mapped[list["Achievement"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )
