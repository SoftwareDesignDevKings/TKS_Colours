from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ── Student ──────────────────────────────────────────────────────────────────

class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    year_group: int = Field(..., ge=7, le=12)
    cohort_year: int = Field(..., ge=2000, le=2100)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    year_group: Optional[int] = Field(None, ge=7, le=12)
    cohort_year: Optional[int] = Field(None, ge=2000, le=2100)
    is_active: Optional[bool] = None


class StudentRead(StudentBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StudentSummary(BaseModel):
    """Lightweight version for list views"""
    id: str
    name: str
    email: str
    year_group: int
    cohort_year: int
    is_active: bool

    model_config = {"from_attributes": True}


# ── Club ─────────────────────────────────────────────────────────────────────

class ClubRead(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str]
    colour: str
    parent_club_id: Optional[str]
    is_active: bool

    model_config = {"from_attributes": True}


class ClubWithSubClubs(ClubRead):
    sub_clubs: list[ClubRead] = []


# ── Criterion ────────────────────────────────────────────────────────────────

class CriterionRead(BaseModel):
    id: str
    club_id: str
    title: str
    description: Optional[str]
    required_count: int
    year_group_applicable: Optional[int]
    sort_order: int
    is_active: bool

    model_config = {"from_attributes": True}


# ── Achievement ──────────────────────────────────────────────────────────────

class AchievementCreate(BaseModel):
    student_id: str
    criterion_id: str
    logged_by_staff_id: Optional[str] = None
    evidence_note: Optional[str] = Field(None, max_length=2000)
    evidence_url: Optional[str] = Field(None, max_length=2048)
    achieved_at: Optional[datetime] = None


class AchievementRead(BaseModel):
    id: str
    student_id: str
    criterion_id: str
    logged_by_staff_id: Optional[str]
    evidence_note: Optional[str]
    evidence_url: Optional[str]
    achieved_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class AchievementWithCriterion(AchievementRead):
    criterion: CriterionRead


# ── Application ──────────────────────────────────────────────────────────────

class ApplicationCreate(BaseModel):
    student_id: str
    club_id: str
    notes: Optional[str] = None
    auto_triggered: bool = False


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    decided_by_id: Optional[str] = None


class ApplicationRead(BaseModel):
    id: str
    student_id: str
    club_id: str
    status: str
    auto_triggered: bool
    notes: Optional[str]
    applied_at: datetime
    decided_at: Optional[datetime]
    decided_by_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApplicationDetail(ApplicationRead):
    student: StudentSummary
    club: ClubRead


# ── Reminder ─────────────────────────────────────────────────────────────────

class ReminderRead(BaseModel):
    id: str
    application_id: str
    staff_id: Optional[str]
    due_at: datetime
    sent_at: Optional[datetime]
    acknowledged_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Staff ────────────────────────────────────────────────────────────────────

class StaffRead(BaseModel):
    id: str
    name: str
    email: str
    role: str
    is_active: bool

    model_config = {"from_attributes": True}


# ── Notification ─────────────────────────────────────────────────────────────

class NotificationRead(BaseModel):
    id: str
    type: str
    title: str
    body: Optional[str]
    student_id: Optional[str]
    application_id: Optional[str]
    club_id: Optional[str]
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime]

    model_config = {"from_attributes": True}


# ── Criteria Engine Response ──────────────────────────────────────────────────

class CriteriaStatus(BaseModel):
    club_id: str
    club_name: str
    total_criteria: int
    met_criteria: int
    is_complete: bool
    criteria_detail: list[dict]
